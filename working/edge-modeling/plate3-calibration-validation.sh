#!/usr/bin/env bash
# plate3-calibration-validation.sh
#
# Mechanical go/no-go validation against working/edge-modeling/plate3-full/
# Designed by sub-agent 4 (general-purpose, Sonnet) on 2026-06-07.
# 7 numeric thresholds + 1 spot-check rule. All must pass for GO.
#
# Run from repo root:  bash working/edge-modeling/plate3-calibration-validation.sh

set -uo pipefail
cd "$(dirname "$0")/../.." 2>/dev/null || cd /Users/mnoth/source/asoiaf-chat

DIR=working/edge-modeling/plate3-full
LEDGER=$DIR/processed-events.jsonl
ROLES=$DIR/role-edges-staging.jsonl
SUPER=$DIR/supersede-candidates.jsonl
REVIEW=$DIR/hub-review-queue.jsonl
MINTED=$DIR/minted-event-nodes
GATEE=$DIR/gate-e-dialogue-recall-skipped.jsonl

[[ -f "$LEDGER" ]] || { echo "FATAL: $LEDGER not found"; exit 1; }

echo "═══════════════════════════════════════════════════════════════"
echo "  Plate 3 Calibration Validation — $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Source: $DIR"
echo "═══════════════════════════════════════════════════════════════"

TOTAL_PROCESSED=$(wc -l <"$LEDGER" | tr -d ' ')
MINTS=$(ls "$MINTED" 2>/dev/null | wc -l | tr -d ' ')
REUSE=$(jq -r 'select(.outcome=="reuse") | 1' "$LEDGER" 2>/dev/null | wc -l | tr -d ' ')
SKIP_DYAD=$(jq -r 'select(.outcome=="skip-clean-dyad") | 1' "$LEDGER" 2>/dev/null | wc -l | tr -d ' ')
BORDERLINE=$(jq -r 'select(.outcome=="borderline-single-agent") | 1' "$LEDGER" 2>/dev/null | wc -l | tr -d ' ')
NON_HARMING=$(jq -r 'select(.outcome=="non-harming-multi-agent") | 1' "$LEDGER" 2>/dev/null | wc -l | tr -d ' ')
ERRORS=$(jq -r 'select(.outcome|startswith("error-")) | 1' "$LEDGER" 2>/dev/null | wc -l | tr -d ' ')
REVIEW_TOTAL=$(wc -l <"$REVIEW" 2>/dev/null | tr -d ' ' || echo 0)
GATEE_SKIPPED=$(wc -l <"$GATEE" 2>/dev/null | tr -d ' ' || echo 0)
ROLE_EDGES_TOTAL=$(wc -l <"$ROLES" 2>/dev/null | tr -d ' ' || echo 0)
SUPER_TOTAL=$(wc -l <"$SUPER" 2>/dev/null | tr -d ' ' || echo 0)

echo ""
echo "── Coverage ──"
echo "  Processed:               $TOTAL_PROCESSED"
echo "  Mints:                   $MINTS"
echo "  Reuse:                   $REUSE"
echo "  Skip clean dyad:         $SKIP_DYAD"
echo "  Borderline single-agent: $BORDERLINE"
echo "  Non-harming multi-agent: $NON_HARMING"
echo "  Errors:                  $ERRORS"
echo "  In review queue:         $REVIEW_TOTAL"
echo "  Gate E pre-rejected:     $GATEE_SKIPPED"
echo "  Role edges total:        $ROLE_EDGES_TOTAL"
echo "  Supersede candidates:    $SUPER_TOTAL"

PASS=0
FAIL=0
WARN=0

check_pass() { echo "  ✓ PASS — $1"; PASS=$((PASS+1)); }
check_fail() { echo "  ✗ FAIL — $1"; FAIL=$((FAIL+1)); }
check_warn() { echo "  ⚠ WARN — $1"; WARN=$((WARN+1)); }

echo ""
echo "── Threshold 1: Contract 10 violation rate = 0% ──"
if [[ $ERRORS -eq 0 ]]; then
  check_pass "0 errors in ledger ($ERRORS)"
else
  check_fail "$ERRORS errors in ledger — investigate before scaling"
fi
TIERS=$(jq -r '.confidence_tier' "$ROLES" 2>/dev/null | sort -u | tr '\n' ',' | sed 's/,$//')
if [[ -n "$TIERS" ]]; then
  echo "  edge confidence tiers seen: $TIERS"
fi

echo ""
echo "── Threshold 2: Mint rate in 15-55% band ──"
DENOM=$((MINTS + REUSE + BORDERLINE + NON_HARMING))
if [[ $DENOM -gt 0 ]]; then
  RATE=$(echo "scale=1; 100*$MINTS/$DENOM" | bc)
  if (( $(echo "$RATE >= 15.0" | bc -l) )) && (( $(echo "$RATE <= 55.0" | bc -l) )); then
    check_pass "mint rate $RATE% in band [15,55]"
  else
    check_warn "mint rate $RATE% outside band [15,55] (denom $DENOM)"
  fi
else
  check_fail "no non-skip outcomes — cannot compute mint rate"
fi

echo ""
echo "── Threshold 3: Role-edge density per minted hub (median ≥3, mean ≥3.5) ──"
if [[ $MINTS -gt 0 ]]; then
  STATS=$(jq -r 'select(.outcome=="mint") | .n_role_edges' "$LEDGER" \
    | sort -n \
    | awk '{a[NR]=$1; s+=$1} END {n=NR; if(n>0){m=(n%2)?a[(n+1)/2]:(a[n/2]+a[n/2+1])/2; printf "%.1f %.1f\n", s/n, m}}')
  MEAN=$(echo "$STATS" | cut -d' ' -f1)
  MED=$(echo "$STATS" | cut -d' ' -f2)
  echo "  mean=$MEAN  median=$MED  (over $MINTS mints)"
  if (( $(echo "$MED >= 3.0" | bc -l) )) && (( $(echo "$MEAN >= 3.5" | bc -l) )); then
    check_pass "density above thresholds"
  else
    check_fail "density below thresholds (need mean≥3.5, median≥3)"
  fi
else
  check_warn "no mints yet — cannot check density"
fi

echo ""
echo "── Threshold 4: ≥80% of minted hubs have ≥2 distinct role types ──"
if [[ $MINTS -gt 0 && $ROLE_EDGES_TOTAL -gt 0 ]]; then
  # For AGENT_IN/VICTIM_IN/COMMANDS_IN/WIELDED_IN: target_slug = event hub.
  # For LOCATED_AT: source_slug = event hub (event LOCATED_AT place).
  # Normalize both into a single "hub<TAB>edge_type" stream, then group by hub.
  DIVERSE=$(jq -r '
    if .edge_type == "LOCATED_AT" then "\(.source_slug)\t\(.edge_type)"
    else "\(.target_slug)\t\(.edge_type)"
    end' "$ROLES" \
    | sort -u \
    | awk -F'\t' '{c[$1]++} END {for(k in c) if(c[k]>=2) print k}' | wc -l | tr -d ' ')
  DIVERSE_PCT=$(echo "scale=1; 100*$DIVERSE/$MINTS" | bc)
  echo "  $DIVERSE / $MINTS mints have ≥2 distinct role types ($DIVERSE_PCT%)"
  if (( $(echo "$DIVERSE_PCT >= 80.0" | bc -l) )); then
    check_pass "diversity above 80%"
  else
    check_fail "diversity below 80% (target band)"
  fi
fi

echo ""
echo "── Threshold 5: Hub-review queue ≤ 25% of processed (target 15%) ──"
if [[ $TOTAL_PROCESSED -gt 0 ]]; then
  REVIEW_PCT=$(echo "scale=1; 100*$REVIEW_TOTAL/$TOTAL_PROCESSED" | bc)
  echo "  review-queue / processed = $REVIEW_PCT%"
  if (( $(echo "$REVIEW_PCT <= 25.0" | bc -l) )); then
    check_pass "review rate $REVIEW_PCT% ≤ 25%"
  else
    check_warn "review rate $REVIEW_PCT% > 25% — borderline detector noisy"
  fi
fi

echo ""
echo "── Threshold 6: Supersede yield ≥ 1.5 per reified (mint+reuse) ──"
REIFIED=$((MINTS + REUSE))
if [[ $REIFIED -gt 0 ]]; then
  RATIO=$(echo "scale=2; $SUPER_TOTAL/$REIFIED" | bc)
  echo "  supersede/reified = $RATIO ($SUPER_TOTAL supersede / $REIFIED reified)"
  if (( $(echo "$RATIO >= 1.5" | bc -l) )); then
    check_pass "supersede yield $RATIO ≥ 1.5"
  else
    check_warn "supersede yield $RATIO < 1.5 — Plate 5 dedup save is small"
  fi
fi

echo ""
echo "── Threshold 7: Cost per reified ≤ \$0.06 (from run.log) ──"
COST=$(grep -oE 'Total LLM cost:[[:space:]]*\$[0-9.]+' "$DIR/run.log" 2>/dev/null | tail -1 | grep -oE '[0-9.]+' | tail -1)
if [[ -n "$COST" && $REIFIED -gt 0 ]]; then
  PER=$(echo "scale=4; $COST/$REIFIED" | bc)
  echo "  total cost \$$COST / reified $REIFIED = \$$PER per reified"
  if (( $(echo "$PER <= 0.06" | bc -l) )); then
    check_pass "cost/reified \$$PER ≤ \$0.06"
  else
    check_warn "cost/reified \$$PER > \$0.06"
  fi
else
  echo "  (cost data not yet in run.log — skip)"
fi

echo ""
echo "── Spot-check: 5 random minted nodes ──"
if [[ $MINTS -gt 0 ]]; then
  SAMPLE=$(ls "$MINTED" | sort -R | head -5)
  for f in $SAMPLE; do
    slug=$(basename "$f" .node.md)
    n_edges=$(jq -r --arg s "$slug" 'select(.target_slug==$s)' "$ROLES" 2>/dev/null | wc -l | tr -d ' ')
    title=$(awk '/^title:/{sub(/^title: */,""); gsub(/"/,""); print; exit}' "$MINTED/$f")
    echo "  - $slug  ($n_edges role edges)  | $title"
  done
  echo "  → manually review these 5: title matches event; AGENT_IN/VICTIM_IN defensible; no edge cited from dialogue *about* event"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Summary: $PASS PASS / $WARN WARN / $FAIL FAIL"
if [[ $FAIL -gt 0 ]]; then
  echo "  → NO-GO. Investigate failures before full sweep."
elif [[ $WARN -gt 2 ]]; then
  echo "  → SOFT NO-GO (>2 warnings). Decide manually."
else
  echo "  → GO if spot-check passes."
fi
echo "═══════════════════════════════════════════════════════════════"
