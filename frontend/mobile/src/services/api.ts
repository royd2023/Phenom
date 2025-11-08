import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

// Configure the base URL - adjust this to your backend URL
const BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api';

interface AnalyzeImageRequest {
  image: string;
  uri: string;
}

interface TestParameter {
  name: string;
  value: string;
  unit: string;
  status: 'normal' | 'abnormal' | 'warning';
  referenceRange: string;
}

interface TestResult {
  id: string;
  timestamp: string;
  status: 'processing' | 'completed' | 'failed';
  overallStatus: 'normal' | 'abnormal' | 'warning';
  parameters: TestParameter[];
  notes?: string;
  imageUri: string;
}

interface TestHistoryResponse {
  tests: TestResult[];
  hasMore: boolean;
  total: number;
}

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_URL,
    prepareHeaders: (headers) => {
      // Add authentication token if available
      const token = ''; // TODO: Get from auth state
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      headers.set('Content-Type', 'application/json');
      return headers;
    },
  }),
  tagTypes: ['TestResult', 'TestHistory'],
  endpoints: (builder) => ({
    analyzeImage: builder.mutation<TestResult, AnalyzeImageRequest>({
      query: (data) => ({
        url: '/analyze',
        method: 'POST',
        body: {
          image: data.image,
        },
      }),
      invalidatesTags: ['TestHistory'],
    }),
    getTestResult: builder.query<TestResult, string>({
      query: (testId) => `/results/${testId}`,
      providesTags: (result, error, testId) => [{ type: 'TestResult', id: testId }],
    }),
    getTestHistory: builder.query<TestHistoryResponse, { page: number; limit: number }>({
      query: ({ page, limit }) => `/history?page=${page}&limit=${limit}`,
      providesTags: ['TestHistory'],
    }),
    deleteTestResult: builder.mutation<void, string>({
      query: (testId) => ({
        url: `/results/${testId}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['TestHistory'],
    }),
  }),
});

export const {
  useAnalyzeImageMutation,
  useGetTestResultQuery,
  useGetTestHistoryQuery,
  useDeleteTestResultMutation,
} = api;
