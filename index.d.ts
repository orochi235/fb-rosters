/** Every name in the corpus, in roster order. */
export declare const NAMES: readonly string[];

/**
 * Draw names from the corpus. Names are dealt from a shuffled deck, so a single
 * call never repeats until all 700 are used up.
 */
export declare function generate(count?: number): string[];
