import type { Config } from "openapi-typescript";

const config: Config = {
  input: process.env.API_SCHEMA_URL ?? "http://localhost:8000/openapi.json",
  output: "src/lib/openapi.d.ts",
  httpMethodName: "request",
};

export default config;
