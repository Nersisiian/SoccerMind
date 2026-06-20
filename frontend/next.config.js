/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/auth/:path*',
        destination: 'http://backend:8000/api/v1/auth/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
