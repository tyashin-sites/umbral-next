/** Typographic wordmark: UMBRAL in the display serif, wide-set, with the A's bar as a threshold. */
export function Wordmark({ className = '' }: { className?: string }) {
  return (
    <span className={`wordmark inline-flex items-baseline font-heading text-[1.35rem] tracking-[0.42em] ${className}`} role="img" aria-label="Umbral">
      <span aria-hidden="true">UMBRAL</span>
    </span>
  );
}
