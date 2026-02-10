/**
 * API Index - Export all API modules
 */

// HTTP Client
export * from './http';

// Movies API
export * from './A2_movies';

// Reviews API
export * from './A6_reviews';

// Profile/User API
export * from './A7_profile';

// Auth API
export * from './auth';

// Re-export for convenience
import * as moviesApi from './A2_movies';
import * as reviewsApi from './A6_reviews';
import * as profileApi from './A7_profile';
import * as authApi from './auth';

export const api = {
  movies: moviesApi,
  reviews: reviewsApi,
  profile: profileApi,
  auth: authApi,
};

export default api;
