import Link from "next/link";

export default function Header() {
  return (
    <header className="bg-black text-white shadow-md">
      <div className="container mx-auto flex justify-between items-center p-4">
        <h1 className="text-xl font-bold text-gold">Anaasɛ Portal</h1>
        <nav className="space-x-6">
          <Link href="/">Home</Link>
          <Link href="/#ghgold">What is GH GOLD</Link>
          <Link href="/#ask">Ask Anaasɛ</Link>
        </nav>
      </div>
    </header>
  );
}
