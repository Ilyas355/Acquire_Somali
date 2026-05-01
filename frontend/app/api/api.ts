import * as SecureStore from 'expo-secure-store';

import type {
  HomeScreenResponse,
  LeaderboardResponse,
  LeaderboardTab,
  LoginRequest,
  LoginResponse,
  PartnerRequestResponse,
  PasswordChangeRequest,
  Profile,
  QuizSubmitRequest,
  QuizSubmitResponse,
  RefreshResponse,
  RegisterRequest,
  RegisterResponse,
  Section,
  StoryCompleteResponse,
  StoryDetail,
  StoryProgressUpdateRequest,
  StoryProgressUpdateResponse,
  StorySummary,
  SubtopicDetail,
  SubtopicProgressUpdateRequest,
  SubtopicProgressUpdateResponse,
  SuggestedPartner,
  UpdateProfileRequest,
  VocabDueItem,
} from '../types/api';

const BASE_URL = process.env.EXPO_PUBLIC_API_URL;

// ─── Token helpers ────────────────────────────────────────────────────────────

export async function storeTokens(access: string, refresh: string): Promise<void> {
  await Promise.all([
    SecureStore.setItemAsync('access_token', access),
    SecureStore.setItemAsync('refresh_token', refresh),
  ]);
}

export async function clearTokens(): Promise<void> {
  await Promise.all([
    SecureStore.deleteItemAsync('access_token'),
    SecureStore.deleteItemAsync('refresh_token'),
  ]);
}

async function getAccessToken(): Promise<string | null> {
  return SecureStore.getItemAsync('access_token');
}

async function refreshAccessToken(): Promise<string> {
  const refresh = await SecureStore.getItemAsync('refresh_token');
  if (!refresh) throw new Error('No refresh token');

  const res = await fetch(`${BASE_URL}/api/auth/token/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  });

  if (!res.ok) {
    await clearTokens();
    throw new Error('Session expired');
  }

  const data: RefreshResponse = await res.json();
  await SecureStore.setItemAsync('access_token', data.access);
  return data.access;
}

// ─── Request helpers ──────────────────────────────────────────────────────────

async function unauthPost<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw await res.json().catch(() => ({ detail: 'Request failed' }));
  return res.json();
}

async function request<T>(
  method: 'GET' | 'POST' | 'PATCH',
  path: string,
  body?: unknown,
): Promise<T> {
  const token = await getAccessToken();
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const options: RequestInit = {
    method,
    headers,
    ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
  };

  let res = await fetch(`${BASE_URL}${path}`, options);

  if (res.status === 401) {
    const newToken = await refreshAccessToken();
    headers['Authorization'] = `Bearer ${newToken}`;
    res = await fetch(`${BASE_URL}${path}`, { ...options, headers });
  }

  if (!res.ok) throw await res.json().catch(() => ({ detail: 'Request failed' }));
  return res.json();
}

// ─── Auth ─────────────────────────────────────────────────────────────────────

export async function register(data: RegisterRequest): Promise<RegisterResponse> {
  return unauthPost('/api/auth/register/', data);
}

export async function login(data: LoginRequest): Promise<LoginResponse> {
  return unauthPost('/api/auth/login/', data);
}

export async function getProfile(): Promise<Profile> {
  return request('GET', '/api/auth/profile/');
}

export async function updateProfile(data: UpdateProfileRequest): Promise<Profile> {
  return request('PATCH', '/api/auth/profile/', data);
}

export async function changePassword(data: PasswordChangeRequest): Promise<void> {
  return request('POST', '/api/auth/password/change/', data);
}

// ─── Curriculum ───────────────────────────────────────────────────────────────

export async function getSections(): Promise<Section[]> {
  return request('GET', '/api/curriculum/sections/');
}

export async function getSubtopic(id: number): Promise<SubtopicDetail> {
  return request('GET', `/api/curriculum/subtopics/${id}/`);
}

// ─── Progress ─────────────────────────────────────────────────────────────────

export async function getHomeScreen(): Promise<HomeScreenResponse> {
  return request('GET', '/api/progress/home/');
}

export async function updateSubtopicProgress(
  id: number,
  data: SubtopicProgressUpdateRequest,
): Promise<SubtopicProgressUpdateResponse> {
  return request('POST', `/api/progress/subtopic/${id}/update/`, data);
}

export async function submitQuiz(data: QuizSubmitRequest): Promise<QuizSubmitResponse> {
  return request('POST', '/api/progress/quiz/submit/', data);
}

export async function getVocabDue(): Promise<VocabDueItem[]> {
  return request('GET', '/api/progress/vocab/due/');
}

// ─── Content ──────────────────────────────────────────────────────────────────

export async function getStories(categoryId?: number): Promise<StorySummary[]> {
  const path = categoryId
    ? `/api/content/stories/?category=${categoryId}`
    : '/api/content/stories/';
  return request('GET', path);
}

export async function getStory(id: number): Promise<StoryDetail> {
  return request('GET', `/api/content/stories/${id}/`);
}

export async function updateStoryProgress(
  id: number,
  data: StoryProgressUpdateRequest,
): Promise<StoryProgressUpdateResponse> {
  return request('PATCH', `/api/content/stories/${id}/progress/`, data);
}

export async function completeStory(id: number): Promise<StoryCompleteResponse> {
  return request('POST', `/api/content/stories/${id}/complete/`);
}

// ─── Community ────────────────────────────────────────────────────────────────

export async function getSuggestedPartners(): Promise<SuggestedPartner[]> {
  return request('GET', '/api/community/partners/suggested/');
}

export async function sendPartnerRequest(userId: number): Promise<PartnerRequestResponse> {
  return request('POST', `/api/community/partners/request/${userId}/`);
}

export async function getLeaderboard(tab: LeaderboardTab = 'all_time'): Promise<LeaderboardResponse> {
  return request('GET', `/api/community/leaderboard/?tab=${tab}`);
}
