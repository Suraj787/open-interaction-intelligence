<script setup>
/* ============================================================================
 * Motif Recipe, Optimistic Save (Vue 3, <script setup>)
 * ----------------------------------------------------------------------------
 * Demonstrates the optimistic-save UX: the UI assumes success the instant the
 * user acts, shows a transient "Saving…" then "Saved", and rolls back to an
 * "error" state only if the (caller-provided) async save rejects.
 *
 * State machine:  idle ──save()──▶ saving ──ok──▶ saved ──(timeout)──▶ idle
 *                                        └──err─▶ error ──retry/save──▶ saving
 *
 * Accessibility:
 *   - A visually-hidden aria-live="polite" region announces each status so
 *     screen-reader users hear "Saving", "Saved", "Couldn't save" etc.
 *   - The button reflects busy state via aria-busy and is disabled while saving.
 *   - Status icon/text use transform+opacity transitions only.
 *
 * Reduced motion:
 *   - usePrefersReducedMotion() + a scoped @media guard. When reduced, the
 *     <Transition> is bypassed (instant state swap) and no transforms run.
 *
 * No external dependencies. The async work is injected via the `saveFn` prop so
 * the component is transport-agnostic and unit-testable.
 * Provenance: original (clean-room).
 * ========================================================================== */
import { ref, computed, onMounted, onUnmounted } from "vue";

const props = defineProps({
  /** Async function performing the real save. Must return a Promise. */
  saveFn: { type: Function, default: () => Promise.resolve() },
  /** Button label in the idle state. */
  label: { type: String, default: "Save" },
  /** How long the "Saved" confirmation lingers before returning to idle (ms). */
  savedDuration: { type: Number, default: 1600 },
  /** Force-disable animation regardless of system preference. */
  disableAnimation: { type: Boolean, default: false },
});

const emit = defineEmits(["stateChange", "saved", "error"]);

/* ---- reduced-motion: live, dependency-free composable -------------------- */
const reducedMotion = ref(false);
let mq;
const onMqChange = (e) => (reducedMotion.value = e.matches);
onMounted(() => {
  if (typeof window === "undefined" || !window.matchMedia) return;
  mq = window.matchMedia("(prefers-reduced-motion: reduce)");
  reducedMotion.value = mq.matches;
  mq.addEventListener?.("change", onMqChange);
});
onUnmounted(() => mq?.removeEventListener?.("change", onMqChange));

/** True when we must not animate (system pref OR explicit opt-out). */
const noMotion = computed(() => props.disableAnimation || reducedMotion.value);
/** Transition name: a no-op when motion is suppressed. */
const transitionName = computed(() => (noMotion.value ? "motif-none" : "motif-status"));

/* ---- state machine ------------------------------------------------------- */
const state = ref("idle"); // 'idle' | 'saving' | 'saved' | 'error'
let savedTimer = null;

const setState = (next) => {
  state.value = next;
  emit("stateChange", next);
};

const clearSavedTimer = () => {
  if (savedTimer) {
    clearTimeout(savedTimer);
    savedTimer = null;
  }
};

async function save() {
  if (state.value === "saving") return; // ignore re-entry while in flight
  clearSavedTimer();
  setState("saving"); // optimistic: show progress immediately

  try {
    await props.saveFn();
    setState("saved");
    emit("saved");
    // Linger on "Saved", then quietly return to idle so the control is reusable.
    savedTimer = setTimeout(() => {
      if (state.value === "saved") setState("idle");
    }, props.savedDuration);
  } catch (err) {
    setState("error");
    emit("error", err);
  }
}

onUnmounted(clearSavedTimer);

/* ---- view helpers -------------------------------------------------------- */
const isBusy = computed(() => state.value === "saving");

/** Human-readable status used for both the visible chip and the live region. */
const statusText = computed(
  () =>
    ({
      idle: "",
      saving: "Saving…",
      saved: "Saved",
      error: "Couldn't save, tap to retry",
    }[state.value])
);

const buttonLabel = computed(() =>
  state.value === "error" ? "Retry" : props.label
);
</script>

<template>
  <div class="motif-optimistic" :data-state="state">
    <button
      type="button"
      class="motif-optimistic__btn"
      :class="{ 'is-error': state === 'error' }"
      :aria-busy="isBusy"
      :disabled="isBusy"
      @click="save"
    >
      {{ buttonLabel }}
    </button>

    <!-- Visual status chip. aria-hidden because the live region below is the
         accessible source of truth (prevents double announcement). -->
    <Transition :name="transitionName">
      <span
        v-if="statusText"
        :key="state"
        class="motif-optimistic__status"
        :class="`is-${state}`"
        aria-hidden="true"
      >
        <span class="motif-optimistic__dot" />
        {{ statusText }}
      </span>
    </Transition>

    <!-- Polite live region: announces status changes without stealing focus. -->
    <span class="motif-sr-only" role="status" aria-live="polite">
      {{ statusText }}
    </span>
  </div>
</template>

<style scoped>
.motif-optimistic {
  display: inline-flex;
  align-items: center;
  gap: 0.625rem;
}

.motif-optimistic__btn {
  font: inherit;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: 1px solid var(--motif-border, #cbd5e1);
  background: var(--motif-accent, #2563eb);
  color: #fff;
  cursor: pointer;
  min-height: 44px; /* coarse-pointer friendly target */
}
.motif-optimistic__btn:disabled {
  cursor: progress;
  opacity: 0.8;
}
.motif-optimistic__btn.is-error {
  background: var(--motif-danger, #dc2626);
}
/* Always keep a visible keyboard focus ring. */
.motif-optimistic__btn:focus-visible {
  outline: 2px solid var(--motif-focus, #1d4ed8);
  outline-offset: 2px;
}

.motif-optimistic__status {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.875rem;
  color: var(--motif-muted, #475569);
}
.motif-optimistic__status.is-error {
  color: var(--motif-danger, #dc2626);
}
.motif-optimistic__status.is-saved {
  color: var(--motif-success, #16a34a);
}

.motif-optimistic__dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: currentColor;
}
/* Subtle pulse while saving, transform/opacity only, motion-safe. */
.is-saving .motif-optimistic__dot {
  animation: motif-pulse 1s ease-in-out infinite;
}

@keyframes motif-pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(0.6);
    opacity: 0.5;
  }
}

/* Enter/leave transition for the status chip (transform + opacity). */
.motif-status-enter-active,
.motif-status-leave-active {
  transition: opacity 200ms ease, transform 200ms ease;
}
.motif-status-enter-from,
.motif-status-leave-to {
  opacity: 0;
  transform: translateY(4px);
}

/* Visually-hidden but screen-reader-available live region. */
.motif-sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
  border: 0;
}

/* Reduced motion: instant state changes, no pulse, no chip transition.
   The `motif-none` transition has no CSS, so <Transition> swaps instantly. */
@media (prefers-reduced-motion: reduce) {
  .motif-optimistic__dot,
  .is-saving .motif-optimistic__dot {
    animation: none !important;
  }
  .motif-status-enter-active,
  .motif-status-leave-active {
    transition: none !important;
  }
  .motif-status-enter-from,
  .motif-status-leave-to {
    transform: none !important;
  }
}
</style>
