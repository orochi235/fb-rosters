/** Names from the 1994 Fighting Baseball roster, in roster order. */
export declare const NAMES: readonly string[];

/** Names from the early-90s celebrity roster, in roster order. */
export declare const CELEBRITIES: readonly string[];

/** Both corpora, by name. */
export declare const ROSTERS: Readonly<{
  athletes: readonly string[];
  celebrities: readonly string[];
}>;

export type RosterName = 'athletes' | 'celebrities' | 'all';

/**
 * Draw names from a corpus. Names are dealt from a shuffled deck, so a single call
 * never repeats until that deck is used up. Each roster keeps its own deck, so
 * drawing from one does not disturb another's no-repeat guarantee.
 *
 * Defaults to the `athletes` roster.
 */
export declare function generate(
  count?: number,
  options?: { roster?: RosterName },
): string[];
