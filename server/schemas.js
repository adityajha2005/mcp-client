import { z } from "zod";

export const ListResourcesRequestSchema = z.object({
  method: z.literal("resources/list"),
});

export const ReadResourceRequestSchema = z.object({
  method: z.literal("resources/read"),
  params: z.object({
    uri: z.string(),
  }),
});

