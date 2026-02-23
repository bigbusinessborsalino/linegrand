import { Link } from "react-router-dom";

const Index = () => {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="text-center">
        <h1 className="font-headline font-bold text-4xl mb-4">Grand Line News</h1>
        <Link to="/" className="text-primary hover:underline font-body">
          Go to Home
        </Link>
      </div>
    </div>
  );
};

export default Index;
