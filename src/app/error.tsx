'use client';
export default function Error({ reset }: { error: Error; reset: () => void }) {
  return (
    <section className="wrap flex min-h-[60vh] flex-col justify-center py-24">
      <h1 className="t-h1">Something stuck.</h1>
      <p className="t-body mt-4">Please try again.</p>
      <button type="button" onClick={reset} className="btn btn-primary mt-8 self-start">Try again <span className="arrow" aria-hidden="true" /></button>
    </section>
  );
}
