export const ListResourcesRequestSchema = {
    type: "object",
    properties: {
      method: { type: "string", enum: ["resources/list"] }, // This needs to match the expected method
    },
  };
  
  export const ReadResourceRequestSchema = {
    type: "object",
    properties: {
      method: { type: "string", enum: ["resources/read"] },  // This needs to match the expected method
      params: {
        type: "object",
        properties: {
          uri: { type: "string" },
        },
      },
    },
  };
  