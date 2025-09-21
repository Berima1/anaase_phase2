import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center h-screen text-center">
      <h1 className="text-6xl font-bold mb-4">404</h1>
      <p className="mb-6">Oops! Page not found.</p>
      <Link href="/" className="bg-gold text-black px-6 py-2 rounded hover:bg-yellow-400">
        Go Home
      </Link>
    </div>
  );
}
