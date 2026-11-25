import Link from 'next/link';

export default function NotFound() {
  return (
    <section className="wrap flex min-h-[70vh] flex-col justify-center py-24">
      <p className="t-num text-[0.8rem] text-bronce">404</p>
      <h1 className="t-display mt-6 max-w-[12ch]">This door does not open.</h1>
      <p className="t-body mt-6">The page you were looking for is not here. The collection is.</p>
      <div className="mt-10"><Link href="/collection" className="btn btn-primary">The collection <span className="arrow" aria-hidden="true" /></Link></div>
    </section>
  );
}
