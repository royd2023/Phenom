import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

// Define the base URL of your backend API
// Use a placeholder as the actual URL is injected via environment variables
const baseUrl = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api';

// Define a service using a base query and expected endpoints.
export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl }),
  tagTypes: ['Analysis', 'History'],
  endpoints: (builder) => ({
    analyzeImage: builder.mutation<any, FormData>({
      query: (formData) => ({
        url: 'analyze',
        method: 'POST',
        body: formData,
      }),
      invalidatesTags: ['History'],
    }),
    getResultById: builder.query<any, string>({
      query: (id) => `results/${id}`,
      providesTags: (result, error, id) => [{ type: 'Analysis', id }],
    }),
    getHistory: builder.query<any[], void>({
      query: () => 'history',
      providesTags: (result) =>
        result
          ? [...result.map(({ id }) => ({ type: 'History' as const, id })), { type: 'History', id: 'LIST' }]
          : [{ type: 'History', id: 'LIST' }],
    }),
    deleteResult: builder.mutation<void, string>({
        query: (id) => ({
            url: `results/${id}`,
            method: 'DELETE',
        }),
        invalidatesTags: (result, error, id) => [{ type: 'History', id: 'LIST' }],
    }),
  }),
});

// Export hooks for usage in functional components, which are
// auto-generated based on the defined endpoints
export const { useAnalyzeImageMutation, useGetResultByIdQuery, useGetHistoryQuery, useDeleteResultMutation } = api;