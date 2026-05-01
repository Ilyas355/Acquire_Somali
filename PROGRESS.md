# Progress

## Done

- Initial Django project scaffolded (`backend/Aquire_Somali/` config, `manage.py`, `requirements.txt`)
- All 5 Django apps created with base files: `models.py`, `views.py`, `admin.py`, `apps.py`, `tests.py`, `migrations/`
- `users/urls.py` created
- Expo frontend scaffolded (`app.json`, `package.json`, `tsconfig.json`, `eslint.config.js`, `expo-env.d.ts`)
- `constants/theme.ts` created
- `components/ui/` created
- All missing files and folders scaffolded (empty): `serializers.py`, `urls.py`, screens, hooks, `api/api.ts`, `types/api.ts`, `context/AuthContext.tsx`, component folders
- `users/models.py` — UserProfile, Level, UserLevel, Achievement, UserAchievement ✓
- `curriculum/models.py` — Section, Subtopic, Phrase, GrammarNote, KeyPattern, CommonMistake, SurvivalLine, QuizQuestion ✓
- `content/models.py` — StoryCategory, Story, StoryLine, StoryTip, UserStoryProgress ✓
- `progress/models.py` — UserSectionProgress, UserSubtopicProgress, QuizAttempt, VocabReview ✓
- `community/models.py` — PartnerRequest, Partner, PartnerProfile, WeeklyChallenge, UserPresence ✓
- `users/serializers.py` — RegisterSerializer, LevelSerializer, UserLevelSerializer, ProfileSerializer ✓
- `users/views.py` — RegisterView, ProfileView, PasswordChangeView ✓
- `users/urls.py` — register, login, token/refresh, profile, password/change ✓
- `Aquire_Somali/urls.py` — root URL config updated to api/auth/ prefix ✓
- `Aquire_Somali/settings.py` — REST_FRAMEWORK JWT config added ✓
- `curriculum/serializers.py` — GrammarNoteSerializer, QuizQuestionSerializer, KeyPatternSerializer, CommonMistakeSerializer, SurvivalLineSerializer, PhraseSerializer, SubtopicSummarySerializer, SubtopicDetailSerializer, SectionSerializer ✓
- `curriculum/views.py` — SectionListView, SubtopicDetailView ✓
- `curriculum/urls.py` — sections/, subtopics/<int:pk>/ ✓
- `progress/serializers.py` — PhraseMinimalSerializer, VocabDueSerializer, SubtopicProgressUpdateSerializer, QuizSubmitSerializer ✓
- `progress/views.py` — HomeScreenView, SubtopicProgressUpdateView, QuizSubmitView, VocabDueView ✓
- `progress/urls.py` — home/, subtopic/<int:pk>/update/, quiz/submit/, vocab/due/ ✓
- `content/serializers.py` — StoryTipSerializer, StoryLineSerializer, StoryCategorySerializer, StoryListSerializer, StoryDetailSerializer ✓
- `content/views.py` — StoryListView, StoryDetailView, StoryProgressUpdateView, StoryCompleteView ✓
- `content/urls.py` — stories/, stories/<int:pk>/, stories/<int:pk>/progress/, stories/<int:pk>/complete/ ✓
- `community/serializers.py` — PartnerProfileSerializer, SuggestedPartnerSerializer, LeaderboardEntrySerializer, WeeklyChallengeSerializer ✓
- `community/views.py` — SuggestedPartnersView, PartnerRequestView, LeaderboardView ✓
- `community/urls.py` — partners/suggested/, partners/request/<int:pk>/, leaderboard/ ✓

---

## In Progress

- Nothing yet

---

## Next

### Phase 1 — Backend

- [x] `users` — `serializers.py`, `views.py`, `urls.py`
- [x] `curriculum` — `serializers.py`, `views.py`, `urls.py`
- [x] `progress` — `serializers.py`, `views.py`, `urls.py`
- [x] `content` — `serializers.py`, `views.py`, `urls.py`
- [x] `community` — `serializers.py`, `views.py`, `urls.py`
- [x] Run migrations across all 5 apps

### Phase 2 — Frontend Foundation

- [x] `types/api.ts` — TypeScript interfaces for every API response
- [x] `api/api.ts` — typed async function per endpoint
- [x] `context/AuthContext.tsx` — global auth state + token logic

### Phase 3 — Auth Flow

- [ ] `app/(auth)/_layout.tsx`
- [ ] `app/(auth)/login.tsx`
- [ ] `app/(auth)/register.tsx`

### Phase 4 — Screens

- [ ] Home — `hooks/useHomeScreen.ts`, `components/home/`, `app/(tabs)/index.tsx`
- [ ] Learn — `hooks/useCurriculum.ts`, `components/learn/`, `app/(tabs)/learn.tsx`
- [ ] Listen — `hooks/useStories.ts`, `components/listen/`, `app/(tabs)/listen.tsx`
- [ ] Community — `hooks/useCommunity.ts`, `components/community/`, `app/(tabs)/community.tsx`
- [ ] Profile — `hooks/useProfile.ts`, `components/profile/`, `app/(tabs)/profile.tsx`

### Phase 5 — Polish

- [ ] Extract shared primitives into `components/ui/` (Button, Card, Input, etc.)
