/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:8000/api/:path*",
      },
      {
        source: "/api/graphql",
        destination: "http://localhost:8000/api/graphql/",
      },
    ];
  },
};

export default nextConfig;