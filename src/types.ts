export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  country: string;
  startDate: string;
  duration: string;
  deadline: string;
  platform: string;
  url: string;
  matchRationale: string;
  skills: string[];
  postedDate: string;
  archived: boolean;
  bookmarked: boolean;
  matchScore: number;
}

export interface JobFilters {
  search: string;
  country: string;
  skill: string;
  platform: string;
}

export interface JobData {
  jobs: Job[];
  lastUpdated: string;
  totalFound: number;
}