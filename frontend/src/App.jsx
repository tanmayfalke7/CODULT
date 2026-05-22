import { useEffect, useMemo, useRef, useState } from 'react'
import axios from 'axios'
import { motion } from 'framer-motion'
import { create } from 'zustand'
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import {
  BarChart3,
  BookOpen,
  BrainCircuit,
  BriefcaseBusiness,
  Check,
  ChevronRight,
  Circle,
  Clock3,
  FileUp,
  GraduationCap,
  LayoutDashboard,
  Lock,
  LogOut,
  Menu,
  Route,
  ShieldCheck,
  Sparkles,
  Target,
  TrendingUp,
  UploadCloud,
  User,
  X,
} from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('career_token')

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

const useAppStore = create((set) => ({
  token: localStorage.getItem('career_token') || '',
  user: JSON.parse(localStorage.getItem('career_user') || 'null'),
  admin: JSON.parse(localStorage.getItem('career_admin') || 'null'),
  studentMode: localStorage.getItem('career_student_mode') === 'true',
  uploadResult: JSON.parse(localStorage.getItem('career_upload_result') || 'null'),
  setSession: ({ token, user }) => {
    localStorage.setItem('career_token', token)
    localStorage.setItem('career_user', JSON.stringify(user))
    localStorage.removeItem('career_admin')
    localStorage.removeItem('career_student_mode')
    set({ token, user, admin: null, studentMode: false })
  },
  setAdminSession: (admin) => {
    localStorage.setItem('career_admin', JSON.stringify(admin))
    localStorage.removeItem('career_token')
    localStorage.removeItem('career_user')
    localStorage.removeItem('career_upload_result')
    localStorage.removeItem('career_student_mode')
    set({ admin, token: '', user: null, studentMode: false, uploadResult: null })
  },
  setStudentMode: () => {
    localStorage.setItem('career_student_mode', 'true')
    localStorage.removeItem('career_token')
    localStorage.removeItem('career_user')
    localStorage.removeItem('career_admin')
    localStorage.removeItem('career_upload_result')
    set({ studentMode: true, token: '', user: null, admin: null, uploadResult: null })
  },
  setUploadResult: (uploadResult) => {
    localStorage.setItem('career_upload_result', JSON.stringify(uploadResult))
    set({ uploadResult })
  },
  logout: () => {
    localStorage.removeItem('career_token')
    localStorage.removeItem('career_user')
    localStorage.removeItem('career_upload_result')
    localStorage.removeItem('career_admin')
    localStorage.removeItem('career_student_mode')
    set({ token: '', user: null, admin: null, studentMode: false, uploadResult: null })
  },
}))

const marketTrends = [
  { role: 'AI Engineer', demand: 94, growth: 41, salary: 26 },
  { role: 'Data Scientist', demand: 88, growth: 32, salary: 20 },
  { role: 'Cloud Architect', demand: 84, growth: 28, salary: 24 },
  { role: 'Cybersecurity Analyst', demand: 91, growth: 36, salary: 18 },
  { role: 'Product Analyst', demand: 73, growth: 22, salary: 15 },
]

const skillRadar = [
  { skill: 'Python', value: 90 },
  { skill: 'ML', value: 75 },
  { skill: 'SQL', value: 64 },
  { skill: 'Cloud', value: 58 },
  { skill: 'Projects', value: 70 },
  { skill: 'Communication', value: 82 },
]

const resourceLibrary = [
  {
    title: 'Machine Learning Specialization',
    provider: 'Coursera',
    type: 'Course',
    level: 'Intermediate',
    focus: 'ML foundations, supervised learning, projects',
  },
  {
    title: 'Google Data Analytics Certificate',
    provider: 'Google',
    type: 'Certification',
    level: 'Beginner',
    focus: 'Analytics, SQL, dashboards, case studies',
  },
  {
    title: 'freeCodeCamp Data Science Track',
    provider: 'YouTube',
    type: 'Playlist',
    level: 'Beginner',
    focus: 'Python, statistics, model building',
  },
  {
    title: 'AWS Cloud Practitioner Essentials',
    provider: 'AWS Skill Builder',
    type: 'Certification',
    level: 'Beginner',
    focus: 'Cloud basics, architecture, deployment',
  },
]

const roleGuidance = {
  school_student: {
    title: 'Beginner career discovery',
    copy: 'Explore broad fields, build study habits, and start tiny portfolio projects.',
  },
  tenth_passout: {
    title: 'Diploma and certificate tracks',
    copy: 'Focus on employable short programs, practical skills, and guided career entry.',
  },
  engineering_student: {
    title: 'Tech and AI acceleration',
    copy: 'Build projects, internships, GitHub proof, and role-specific interview readiness.',
  },
  college_student: {
    title: 'Portfolio-first career planning',
    copy: 'Turn coursework into career evidence with skills, projects, and learning paths.',
  },
  working_professional: {
    title: 'Career switching strategy',
    copy: 'Map transferable skills, close gaps, and stage a realistic transition roadmap.',
  },
  career_switcher: {
    title: 'Focused transition roadmap',
    copy: 'Choose adjacent roles, build proof fast, and track momentum every week.',
  },
}

const fallbackRoadmapSteps = [
  { id: 1, title: 'Foundation skills', status: 'completed', completion_percentage: 100 },
  { id: 2, title: 'Core tools', status: 'in_progress', completion_percentage: 55 },
  { id: 3, title: 'Portfolio project', status: 'not_started', completion_percentage: 0 },
  { id: 4, title: 'Certification sprint', status: 'not_started', completion_percentage: 0 },
  { id: 5, title: 'Interview preparation', status: 'not_started', completion_percentage: 0 },
]

const quizQuestions = [
  {
    question: 'When faced with a broken gadget at home, what is your first instinct?',
    options: [
      ['A', 'Take it apart to see how the physical pieces fit together and try to fix it manually.', 'Realistic'],
      ['B', 'Look closely at the circuits or research online to understand the scientific reason it stopped working.', 'Investigative'],
      ['C', 'Think about how you could redesign the outside of it so it looks cooler.', 'Artistic'],
      ['D', 'Ask a family member or friend to help you, so you can figure it out together.', 'Social'],
    ],
  },
  {
    question: 'In a group project at school, which role do you naturally take on?',
    options: [
      ['A', 'The doer who wants to build the actual model, poster, or physical presentation.', 'Realistic'],
      ['B', 'The researcher who dives deep into the library or internet to find complex facts and data.', 'Investigative'],
      ['C', 'The director who takes charge, assigns tasks, and motivates the team.', 'Enterprising'],
      ['D', 'The organizer who creates the schedule and makes sure everyone meets the deadline.', 'Conventional'],
    ],
  },
  {
    question: 'If you have a completely free Saturday afternoon, how are you most likely to spend it?',
    options: [
      ['A', 'Building a DIY project, fixing a bike, coding a simple game, or playing a sport.', 'Realistic'],
      ['B', 'Watching a documentary, reading about a new topic, or doing a science experiment.', 'Investigative'],
      ['C', 'Sketching, writing a story, playing a musical instrument, or editing a video.', 'Artistic'],
      ['D', 'Volunteering, hanging out with friends, or helping someone with their homework.', 'Social'],
    ],
  },
  {
    question: 'Which of these sounds like the best work environment for your future?',
    options: [
      ['A', 'Outdoors, in a workshop, or a place where I can move around and use tools.', 'Realistic'],
      ['B', 'A quiet laboratory, university, or research center where I can study the world.', 'Investigative'],
      ['C', 'A busy corporate office where I am pitching new ideas, traveling, and leading meetings.', 'Enterprising'],
      ['D', 'A clean, well-organized office with clear rules, predictable tasks, and structured data.', 'Conventional'],
    ],
  },
  {
    question: 'When learning a new subject, what do you enjoy most?',
    options: [
      ['A', 'Doing hands-on activities, labs, or practical applications of the subject.', 'Realistic'],
      ['B', 'Discovering the why behind things and analyzing complex theories.', 'Investigative'],
      ['C', 'Coming up with highly creative ideas that challenge the normal way of thinking.', 'Artistic'],
      ['D', 'Discussing the subject with classmates, debating, and hearing human perspectives.', 'Social'],
    ],
  },
  {
    question: 'What is most important to you when thinking about your future success?',
    options: [
      ['A', 'Being recognized as a master of a physical, technical, or athletic skill.', 'Realistic'],
      ['B', 'Having the freedom to express my individuality and imagination.', 'Artistic'],
      ['C', 'Achieving status, earning a strong income, and leading a large group of people.', 'Enterprising'],
      ['D', 'Helping people, making a difference, and being known as a kind person.', 'Social'],
    ],
  },
  {
    question: 'Which pair of school subjects do you look forward to the most?',
    options: [
      ['A', 'Shop class, physical education, or practical science labs.', 'Realistic'],
      ['B', 'Advanced math, biology, chemistry, or computer science.', 'Investigative'],
      ['C', 'Art, drama, music, or creative writing.', 'Artistic'],
      ['D', 'Debate, business, economics, or speech.', 'Enterprising'],
    ],
  },
  {
    question: 'How do you feel about rules and instructions?',
    options: [
      ['A', 'I like them when they show me step-by-step how to build something physical.', 'Realistic'],
      ['B', 'I follow them only if they logically make sense after I analyze them.', 'Investigative'],
      ['C', 'I prefer to bend them; I like doing things my own unique way.', 'Artistic'],
      ['D', 'I like them; they keep things orderly and clear.', 'Conventional'],
    ],
  },
  {
    question: 'When your friends are having an argument, how do you handle it?',
    options: [
      ['A', 'I stay out of it; I prefer practical tasks over emotional drama.', 'Realistic'],
      ['B', 'I analyze the situation logically and figure out who is factually right.', 'Investigative'],
      ['C', 'I listen to both sides and try to help them heal their friendship.', 'Social'],
      ['D', 'I step in and take control, convincing them to agree to a compromise.', 'Enterprising'],
    ],
  },
  {
    question: 'How do you want to leave your mark on the world?',
    options: [
      ['A', 'By building a physical structure, technology, or system that lasts.', 'Realistic'],
      ['B', 'By inventing a scientific theory, discovering a cure, or solving a complex problem.', 'Investigative'],
      ['C', 'By creating art, music, or literature that moves people emotionally.', 'Artistic'],
      ['D', 'By building a highly successful company or organization.', 'Enterprising'],
    ],
  },
]

const quizProfiles = {
  Realistic: {
    label: 'The Doers',
    description: 'You like working with your hands, tools, machines, systems, and practical challenges.',
    careers: ['Engineer', 'Architect', 'Mechanic', 'Computer Technician', 'Athlete', 'Pilot', 'Environmental Scientist'],
  },
  Investigative: {
    label: 'The Thinkers',
    description: 'You are analytical, curious, scientific, and drawn to solving complex questions.',
    careers: ['Software Developer', 'Biologist', 'Chemist', 'Data Analyst', 'Psychologist', 'Researcher', 'Surgeon'],
  },
  Artistic: {
    label: 'The Creators',
    description: 'You are creative, original, expressive, and enjoy independent imagination.',
    careers: ['Graphic Designer', 'Writer', 'Musician', 'Film Director', 'UX/UI Designer', 'Animator', 'Interior Designer'],
  },
  Social: {
    label: 'The Helpers',
    description: 'You enjoy working with people, teaching, supporting, and helping communities.',
    careers: ['Teacher', 'Counselor', 'Physical Therapist', 'Nurse', 'Social Worker', 'Human Resources Manager'],
  },
  Enterprising: {
    label: 'The Persuaders',
    description: 'You are ambitious, energetic, persuasive, and comfortable leading people.',
    careers: ['Entrepreneur', 'Business Manager', 'Lawyer', 'Marketing Director', 'Real Estate Agent', 'Politician'],
  },
  Conventional: {
    label: 'The Organizers',
    description: 'You are detail-oriented, structured, organized, and comfortable with data and rules.',
    careers: ['Accountant', 'Financial Analyst', 'Project Manager', 'Data Entry Specialist', 'Actuary', 'Logistics Coordinator'],
  },
}

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

function Button({ children, variant = 'primary', className = '', ...props }) {
  const variants = {
    primary: 'bg-[#6f7f45] text-white hover:bg-[#596739]',
    secondary: 'bg-[#d7edf7] text-[#163142] hover:bg-[#c6e5f2]',
    ghost: 'bg-white text-[#26341f] border border-[#dfe8d7] hover:bg-[#f3f7ef]',
    warm: 'bg-[#f4d35e] text-[#2f2b12] hover:bg-[#e9c746]',
  }

  return (
    <button
      className={classNames(
        'inline-flex min-h-11 items-center justify-center gap-2 rounded-md px-4 py-2 text-sm font-semibold transition shadow-sm',
        variants[variant],
        className,
      )}
      {...props}
    >
      {children}
    </button>
  )
}

function Pill({ children, tone = 'olive' }) {
  const tones = {
    olive: 'bg-[#eef4e8] text-[#536431]',
    sky: 'bg-[#e8f6fb] text-[#27556d]',
    yellow: 'bg-[#fff6c8] text-[#7a6414]',
  }

  return (
    <span className={classNames('rounded-full px-3 py-1 text-xs font-semibold', tones[tone])}>
      {children}
    </span>
  )
}

function StatCard({ icon: Icon, label, value, hint, tone = 'olive' }) {
  const iconTone = {
    olive: 'bg-[#eef4e8] text-[#66773f]',
    sky: 'bg-[#e8f6fb] text-[#35708c]',
    yellow: 'bg-[#fff6c8] text-[#89701b]',
  }

  return (
    <div className="metric-card rounded-lg p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-[#69725f]">{label}</p>
          <p className="mt-2 text-3xl font-bold text-[#17201a]">{value}</p>
        </div>
        <div className={classNames('rounded-md p-3', iconTone[tone])}>
          <Icon size={20} />
        </div>
      </div>
      <p className="mt-3 text-sm text-[#727b68]">{hint}</p>
    </div>
  )
}

function Header({ activePage, setActivePage }) {
  const { user, token, admin, studentMode, logout } = useAppStore()
  const [open, setOpen] = useState(false)

  const isSchoolStudent = studentMode || user?.profile_type === 'school_student'
  const navItems = admin
    ? [
        ['landing', 'Home'],
        ['admin', 'Admin'],
        ['trends', 'Trends'],
      ]
    : isSchoolStudent
      ? [
          ['landing', 'Home'],
          ['student-dashboard', 'Career Quiz'],
        ]
      : [
          ['landing', 'Home'],
          ['upload', 'Upload'],
          ['dashboard', 'Dashboard'],
          ['roadmap', 'Roadmap'],
          ['trends', 'Trends'],
        ]

  const navigate = (page) => {
    setActivePage(page)
    setOpen(false)
  }

  return (
    <header className="sticky top-0 z-40 border-b border-[#dfe8d7] bg-[#f8faf7]/90 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
        <button className="flex items-center gap-3" onClick={() => navigate('landing')}>
          <span className="flex size-10 items-center justify-center rounded-md bg-[#6f7f45] text-white">
            <BrainCircuit size={22} />
          </span>
          <span className="text-left">
            <span className="block text-base font-bold text-[#17201a]">CareerPilot AI</span>
            <span className="block text-xs font-medium text-[#6d7664]">Resume to roadmap</span>
          </span>
        </button>

        <nav className="hidden items-center gap-1 lg:flex">
          {navItems.map(([page, label]) => (
            <button
              key={page}
              className={classNames(
                'rounded-md px-3 py-2 text-sm font-semibold transition',
                activePage === page
                  ? 'bg-white text-[#536431] shadow-sm'
                  : 'text-[#5f6958] hover:bg-white/70 hover:text-[#17201a]',
              )}
              onClick={() => navigate(page)}
            >
              {label}
            </button>
          ))}
        </nav>

        <div className="hidden items-center gap-3 lg:flex">
          {token || admin ? (
            <>
              <div className="flex items-center gap-2 rounded-md bg-white px-3 py-2 text-sm font-semibold text-[#536431]">
                <User size={16} />
                {admin?.username || user?.first_name || 'User'}
              </div>
              <Button
                variant="ghost"
                onClick={() => {
                  logout()
                  setActivePage('landing')
                }}
              >
                <LogOut size={16} /> Logout
              </Button>
            </>
          ) : (
            <Button onClick={() => navigate('role-select')}>
              <ShieldCheck size={16} /> Sign in
            </Button>
          )}
        </div>

        <button
          className="inline-flex size-10 items-center justify-center rounded-md bg-white text-[#536431] lg:hidden"
          onClick={() => setOpen((value) => !value)}
          aria-label="Toggle navigation"
        >
          {open ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {open && (
        <div className="border-t border-[#dfe8d7] bg-[#f8faf7] px-4 py-3 lg:hidden">
          <div className="grid gap-2">
            {navItems.map(([page, label]) => (
              <button
                key={page}
                className="rounded-md bg-white px-3 py-3 text-left text-sm font-semibold text-[#536431]"
                onClick={() => navigate(page)}
              >
                {label}
              </button>
            ))}
            <Button variant={token || admin ? 'ghost' : 'primary'} onClick={() => (token || admin ? logout() : navigate('role-select'))}>
              {token || admin ? 'Logout' : 'Sign in'}
            </Button>
          </div>
        </div>
      )}
    </header>
  )
}

function LandingPage({ setActivePage }) {
  const features = [
    ['Resume intelligence', 'Extracts skills, education, interests, and certifications from uploaded resumes.', FileUp],
    ['Career matching', 'Compares your profile against ML career embeddings and ranks best-fit roles.', Target],
    ['Roadmap builder', 'Turns the top recommendation into a step-by-step learning path.', Route],
    ['Market trends', 'Surfaces demand, growth, and skill direction for judging-ready analytics.', TrendingUp],
  ]

  return (
    <main>
      <section className="soft-grid">
        <div className="mx-auto grid max-w-7xl items-center gap-10 px-4 py-12 sm:px-6 lg:grid-cols-[1.05fr_0.95fr] lg:px-8 lg:py-16">
          <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}>
            <div className="flex flex-wrap gap-2">
              <Pill tone="olive">AI career recommender</Pill>
              <Pill tone="sky">JWT dashboard</Pill>
              <Pill tone="yellow">Hackathon ready</Pill>
            </div>
            <h1 className="mt-6 max-w-3xl text-4xl font-bold leading-tight text-[#17201a] sm:text-5xl lg:text-6xl">
              Convert one resume into a clear career path.
            </h1>
            <p className="mt-5 max-w-2xl text-lg leading-8 text-[#5f6958]">
              Upload a resume, extract skills, predict career matches, generate a roadmap, and track progress in one clean workspace.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Button className="min-w-40" onClick={() => setActivePage('upload')}>
                <UploadCloud size={18} /> Upload resume
              </Button>
              <Button variant="secondary" onClick={() => setActivePage('dashboard')}>
                <LayoutDashboard size={18} /> View dashboard
              </Button>
              <Button variant="ghost" onClick={() => setActivePage('role-select')}>
                <ShieldCheck size={18} /> Choose role
              </Button>
            </div>
          </motion.div>

          <motion.div
            className="glass-panel rounded-lg p-5"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.12 }}
          >
            <div className="rounded-lg bg-[#17201a] p-5 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-[#cfe4bd]">Live career signal</p>
                  <h2 className="mt-1 text-2xl font-bold">AI Engineer</h2>
                </div>
                <Sparkles className="text-[#f4d35e]" />
              </div>
              <div className="mt-6 h-52">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={marketTrends}>
                    <defs>
                      <linearGradient id="demandFill" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#f4d35e" stopOpacity={0.9} />
                        <stop offset="95%" stopColor="#8ecae6" stopOpacity={0.05} />
                      </linearGradient>
                    </defs>
                    <XAxis dataKey="role" hide />
                    <YAxis hide domain={[0, 100]} />
                    <Tooltip />
                    <Area type="monotone" dataKey="demand" stroke="#f4d35e" fill="url(#demandFill)" strokeWidth={3} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 grid grid-cols-3 gap-2 text-xs font-semibold text-[#d7edf7]">
                <span>High demand</span>
                <span className="text-center">Growth roles</span>
                <span className="text-right">Salary lift</span>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="mb-6 grid gap-4 md:grid-cols-2">
          <button
            className="metric-card rounded-lg p-5 text-left transition hover:-translate-y-1 hover:border-[#8ecae6]"
            onClick={() => setActivePage('auth')}
          >
            <Pill tone="olive">Student or professional</Pill>
            <h2 className="mt-4 text-2xl font-bold text-[#17201a]">I am not an admin</h2>
            <p className="mt-2 text-sm leading-6 text-[#69725f]">Create a user account for resume analysis, dashboard, roadmap, or school career quiz.</p>
          </button>
          <button
            className="metric-card rounded-lg p-5 text-left transition hover:-translate-y-1 hover:border-[#f4d35e]"
            onClick={() => setActivePage('admin-login')}
          >
            <Pill tone="yellow">Admin access</Pill>
            <h2 className="mt-4 text-2xl font-bold text-[#17201a]">I am an admin</h2>
            <p className="mt-2 text-sm leading-6 text-[#69725f]">Use the separate admin login with username and password only.</p>
          </button>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {features.map(([title, copy, Icon]) => (
            <div key={title} className="metric-card rounded-lg p-5">
              <Icon className="text-[#6f7f45]" size={24} />
              <h3 className="mt-4 text-lg font-bold text-[#17201a]">{title}</h3>
              <p className="mt-2 text-sm leading-6 text-[#69725f]">{copy}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}

function AuthPage({ setActivePage }) {
  const { setSession } = useAppStore()
  const [mode, setMode] = useState('login')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [form, setForm] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    profile_type: 'engineering_student',
  })

  const submit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setMessage('')

    if (mode === 'forgot') {
      setMessage('Password reset flow is ready for backend email integration.')
      setLoading(false)
      return
    }

    try {
      const endpoint = mode === 'login' ? '/auth/login' : '/auth/register'
      const payload =
        mode === 'login'
          ? { email: form.email, password: form.password }
          : form
      const { data } = await api.post(endpoint, payload)

      setSession({
        token: data.access_token,
        user: data.user,
      })
      setActivePage(data.user?.profile_type === 'school_student' ? 'student-dashboard' : 'dashboard')
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Could not complete authentication.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="mx-auto grid min-h-[calc(100vh-80px)] max-w-6xl items-center gap-8 px-4 py-10 sm:px-6 lg:grid-cols-[0.9fr_1.1fr] lg:px-8">
      <section>
        <Pill tone="sky">Protected APIs</Pill>
        <h1 className="mt-5 text-4xl font-bold leading-tight text-[#17201a]">Secure career workspace.</h1>
        <p className="mt-4 text-lg leading-8 text-[#5f6958]">
          Create a JWT-backed account, upload resumes, and keep your roadmap progress tied to your profile.
        </p>
        <div className="mt-8 grid gap-3">
          {['JWT access tokens', 'PBKDF2 password hashing', 'Protected dashboard routes'].map((item) => (
            <div key={item} className="flex items-center gap-3 rounded-lg bg-white p-4 text-sm font-semibold text-[#536431]">
              <Check size={18} /> {item}
            </div>
          ))}
        </div>
      </section>

      <form className="glass-panel rounded-lg p-6" onSubmit={submit}>
        <div className="flex rounded-md bg-[#eef4e8] p-1">
          <button
            type="button"
            className={classNames('flex-1 rounded-md px-3 py-2 text-sm font-bold', mode === 'login' && 'bg-white text-[#536431] shadow-sm')}
            onClick={() => setMode('login')}
          >
            Login
          </button>
          <button
            type="button"
            className={classNames('flex-1 rounded-md px-3 py-2 text-sm font-bold', mode === 'register' && 'bg-white text-[#536431] shadow-sm')}
            onClick={() => setMode('register')}
          >
            Register
          </button>
        </div>

        <div className="mt-6 grid gap-4">
          {mode === 'register' && (
            <div className="grid gap-4 sm:grid-cols-2">
              <Input label="First name" value={form.first_name} onChange={(value) => setForm({ ...form, first_name: value })} />
              <Input label="Last name" value={form.last_name} onChange={(value) => setForm({ ...form, last_name: value })} />
            </div>
          )}
          <Input label="Email" type="email" value={form.email} onChange={(value) => setForm({ ...form, email: value })} required />
          {mode !== 'forgot' && (
            <Input label="Password" type="password" value={form.password} onChange={(value) => setForm({ ...form, password: value })} required />
          )}
          {mode === 'register' && (
            <label className="grid gap-2 text-sm font-semibold text-[#536431]">
              Profile type
              <select
                className="min-h-11 rounded-md border border-[#dfe8d7] bg-white px-3 text-[#17201a] outline-none focus:border-[#8ecae6]"
                value={form.profile_type}
                onChange={(event) => setForm({ ...form, profile_type: event.target.value })}
              >
                {Object.keys(roleGuidance).map((type) => (
                  <option key={type} value={type}>
                    {type.replaceAll('_', ' ')}
                  </option>
                ))}
              </select>
            </label>
          )}
          <Button disabled={loading} className="w-full">
            <ShieldCheck size={18} /> {loading ? 'Please wait...' : mode === 'login' ? 'Login' : mode === 'forgot' ? 'Send reset link' : 'Create account'}
          </Button>
          <button
            type="button"
            className="text-sm font-semibold text-[#35708c]"
            onClick={() => setMode(mode === 'forgot' ? 'login' : 'forgot')}
          >
            {mode === 'forgot' ? 'Back to login' : 'Forgot password'}
          </button>
          {message && <p className="rounded-md bg-[#fff6c8] p-3 text-sm font-semibold text-[#7a6414]">{message}</p>}
        </div>
      </form>
    </main>
  )
}

function RoleSelectPage({ setActivePage }) {
  const { setStudentMode } = useAppStore()

  return (
    <main className="mx-auto grid min-h-[calc(100vh-80px)] max-w-7xl items-center gap-6 px-4 py-10 sm:px-6 lg:grid-cols-3 lg:px-8">
      <button
        className="glass-panel rounded-lg p-7 text-left transition hover:-translate-y-1 hover:border-[#8ecae6]"
        onClick={() => {
          setStudentMode()
          setActivePage('student-dashboard')
        }}
      >
        <Pill tone="sky">School student</Pill>
        <h1 className="mt-5 text-3xl font-bold text-[#17201a]">Career quiz only</h1>
        <p className="mt-3 leading-7 text-[#5f6958]">
          No backend login, no resume upload. Attempt the exploration quiz as many times as you want.
        </p>
        <span className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-[#27556d]">
          Start quiz <ChevronRight size={16} />
        </span>
      </button>

      <button
        className="glass-panel rounded-lg p-7 text-left transition hover:-translate-y-1 hover:border-[#8ecae6]"
        onClick={() => setActivePage('auth')}
      >
        <Pill tone="olive">User login</Pill>
        <h1 className="mt-5 text-3xl font-bold text-[#17201a]">College or professional</h1>
        <p className="mt-3 leading-7 text-[#5f6958]">
          Use email and password for resume analysis, recommendations, dashboard, and roadmap tracking.
        </p>
        <span className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-[#536431]">
          Continue as user <ChevronRight size={16} />
        </span>
      </button>

      <button
        className="glass-panel rounded-lg p-7 text-left transition hover:-translate-y-1 hover:border-[#f4d35e]"
        onClick={() => setActivePage('admin-login')}
      >
        <Pill tone="yellow">Admin login</Pill>
        <h1 className="mt-5 text-3xl font-bold text-[#17201a]">Administrator</h1>
        <p className="mt-3 leading-7 text-[#5f6958]">
          Use a separate username and password flow for managing trends, skills, analytics, and learning resources.
        </p>
        <span className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-[#7a6414]">
          Continue as admin <ChevronRight size={16} />
        </span>
      </button>
    </main>
  )
}

function AdminLoginPage({ setActivePage }) {
  const { setAdminSession } = useAppStore()
  const [form, setForm] = useState({
    username: '',
    password: '',
  })
  const [message, setMessage] = useState('')

  const submit = (event) => {
    event.preventDefault()
    setMessage('')

    if (form.username === 'admin' && form.password === 'admin123') {
      setAdminSession({
        username: 'admin',
        role: 'admin',
      })
      setActivePage('admin')
      return
    }

    setMessage('Invalid admin username or password.')
  }

  return (
    <main className="mx-auto grid min-h-[calc(100vh-80px)] max-w-6xl items-center gap-8 px-4 py-10 sm:px-6 lg:grid-cols-[0.9fr_1.1fr] lg:px-8">
      <section>
        <Pill tone="yellow">Separate admin access</Pill>
        <h1 className="mt-5 text-4xl font-bold leading-tight text-[#17201a]">Admin login</h1>
        <p className="mt-4 text-lg leading-8 text-[#5f6958]">
          This panel is separate from user authentication and uses only username and password.
        </p>
        <div className="mt-8 rounded-lg bg-[#fff6c8] p-4 text-sm font-semibold text-[#7a6414]">
          Demo credentials: username admin, password admin123
        </div>
      </section>

      <form className="glass-panel rounded-lg p-6" onSubmit={submit}>
        <div className="grid gap-4">
          <Input label="Username" value={form.username} onChange={(value) => setForm({ ...form, username: value })} required />
          <Input label="Password" type="password" value={form.password} onChange={(value) => setForm({ ...form, password: value })} required />
          <Button className="w-full" variant="warm">
            <ShieldCheck size={18} /> Login as admin
          </Button>
          <Button type="button" variant="ghost" onClick={() => setActivePage('role-select')}>
            Back
          </Button>
          {message && <p className="rounded-md bg-[#fff6c8] p-3 text-sm font-semibold text-[#7a6414]">{message}</p>}
        </div>
      </form>
    </main>
  )
}

function Input({ label, value, onChange, type = 'text', required = false }) {
  return (
    <label className="grid gap-2 text-sm font-semibold text-[#536431]">
      {label}
      <input
        className="min-h-11 rounded-md border border-[#dfe8d7] bg-white px-3 text-[#17201a] outline-none transition focus:border-[#8ecae6] focus:ring-4 focus:ring-[#d7edf7]"
        type={type}
        value={value}
        required={required}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  )
}

function UploadPage({ setActivePage }) {
  const { token, user, studentMode, setUploadResult } = useAppStore()
  const inputRef = useRef(null)
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const upload = async () => {
    if (studentMode || user?.profile_type === 'school_student') {
      setActivePage('student-dashboard')
      return
    }

    if (!token) {
      setActivePage('auth')
      return
    }

    if (!file) {
      setMessage('Choose a resume file first.')
      return
    }

    const formData = new FormData()
    formData.append('file', file)
    setLoading(true)
    setMessage('')

    try {
      const { data } = await api.post('/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setUploadResult(data)
      setActivePage('results')
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Upload pipeline failed. Check backend logs and API keys.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="grid gap-8 lg:grid-cols-[0.9fr_1.1fr]">
        <section>
          <Pill tone="olive">Main orchestration endpoint</Pill>
          <h1 className="mt-5 text-4xl font-bold leading-tight text-[#17201a]">Upload resume, trigger the full AI pipeline.</h1>
          <p className="mt-4 text-lg leading-8 text-[#5f6958]">
            This calls `/resume/upload`, then stores resume data, skills, recommendations, roadmap, and analytics.
          </p>
          <Pipeline />
        </section>

        <section className="glass-panel rounded-lg p-6">
          <div
            className="flex min-h-72 flex-col items-center justify-center rounded-lg border-2 border-dashed border-[#b9c9aa] bg-white p-8 text-center transition hover:border-[#8ecae6]"
            onDragOver={(event) => event.preventDefault()}
            onDrop={(event) => {
              event.preventDefault()
              setFile(event.dataTransfer.files?.[0] || null)
            }}
          >
            <UploadCloud className="text-[#6f7f45]" size={44} />
            <h2 className="mt-5 text-2xl font-bold text-[#17201a]">Drop your resume here</h2>
            <p className="mt-2 max-w-md text-sm leading-6 text-[#69725f]">Supports PDF, DOCX, and TXT files.</p>
            <input
              ref={inputRef}
              className="hidden"
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={(event) => setFile(event.target.files?.[0] || null)}
            />
            <Button className="mt-6" variant="secondary" onClick={() => inputRef.current?.click()}>
              <FileUp size={18} /> Browse file
            </Button>
            {file && <p className="mt-4 rounded-md bg-[#eef4e8] px-3 py-2 text-sm font-semibold text-[#536431]">{file.name}</p>}
          </div>
          <div className="mt-5 flex flex-col gap-3 sm:flex-row">
            <Button className="flex-1" disabled={loading} onClick={upload}>
              <Sparkles size={18} /> {loading ? 'Running pipeline...' : 'Analyze resume'}
            </Button>
            <Button className="flex-1" variant="ghost" onClick={() => setFile(null)}>
              Clear
            </Button>
          </div>
          {message && <p className="mt-4 rounded-md bg-[#fff6c8] p-3 text-sm font-semibold text-[#7a6414]">{message}</p>}
        </section>
      </div>
    </main>
  )
}

function Pipeline() {
  const steps = ['Upload', 'Extract', 'LLM parse', 'Save skills', 'Recommend', 'Roadmap', 'Analytics']

  return (
    <div className="mt-8 grid gap-3">
      {steps.map((step, index) => (
        <div key={step} className="flex items-center gap-3 rounded-lg bg-white p-4 shadow-sm">
          <span className="flex size-8 shrink-0 items-center justify-center rounded-md bg-[#eef4e8] text-sm font-bold text-[#536431]">
            {index + 1}
          </span>
          <span className="text-sm font-semibold text-[#26341f]">{step}</span>
          {index < steps.length - 1 && <ChevronRight className="ml-auto text-[#9eaa95]" size={18} />}
        </div>
      ))}
    </div>
  )
}

function ResultsPage() {
  const { uploadResult } = useAppStore()
  const matches = uploadResult?.top_career_matches || marketTrends.slice(0, 3).map((item) => ({
    career: item.role,
    similarity_score: item.demand / 100,
  }))

  return (
    <main className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <Pill tone="yellow">Recommendation results</Pill>
          <h1 className="mt-4 text-4xl font-bold text-[#17201a]">{uploadResult?.recommended_career || 'AI Engineer'}</h1>
          <p className="mt-3 max-w-2xl text-[#5f6958]">Career matches, confidence scores, explanation, and salary signals from the latest analysis.</p>
        </div>
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_0.85fr]">
        <section className="glass-panel rounded-lg p-5">
          <h2 className="text-xl font-bold text-[#17201a]">Career match comparison</h2>
          <div className="mt-5 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={matches.map((item) => ({ name: item.career, score: Math.round(item.similarity_score * 100) }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e4eadf" />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Bar dataKey="score" radius={[6, 6, 0, 0]}>
                  {matches.map((item, index) => (
                    <Cell key={item.career} fill={['#6f7f45', '#8ecae6', '#f4d35e', '#a8b88d', '#5798b8'][index % 5]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="grid gap-4">
          {matches.map((item, index) => (
            <div key={item.career} className="metric-card rounded-lg p-5">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-xs font-bold uppercase tracking-wide text-[#8a957d]">Rank {index + 1}</p>
                  <h3 className="mt-1 text-lg font-bold text-[#17201a]">{item.career}</h3>
                </div>
                <span className="rounded-md bg-[#eef4e8] px-3 py-2 text-sm font-bold text-[#536431]">
                  {Math.round(item.similarity_score * 100)}%
                </span>
              </div>
              <p className="mt-3 text-sm leading-6 text-[#69725f]">Strong match based on skill overlap, education context, and interest signals from the resume.</p>
            </div>
          ))}
        </section>
      </div>
    </main>
  )
}

function DashboardPage({ setActivePage }) {
  const { user, uploadResult, token, studentMode } = useAppStore()
  const [dashboardData, setDashboardData] = useState(null)
  const [apiActivities, setApiActivities] = useState([])
  const guidance = roleGuidance[user?.profile_type] || roleGuidance.engineering_student
  const matches = uploadResult?.top_career_matches || []

  useEffect(() => {
    if (!token) {
      return
    }

    const loadDashboard = async () => {
      try {
        const [{ data: dashboard }, { data: activities }] = await Promise.all([
          api.get('/dashboard'),
          api.get('/dashboard/activities'),
        ])
        setDashboardData(dashboard)
        setApiActivities(activities)
      } catch {
        setDashboardData(null)
      }
    }

    loadDashboard()
  }, [token])

  const activities = apiActivities.length
    ? apiActivities.map((activity) => activity.description || activity.type)
    : ['Resume uploaded', 'Career recommendations generated', 'Roadmap created', 'Dashboard analytics updated']

  if (studentMode || user?.profile_type === 'school_student') {
    return <SchoolStudentDashboard />
  }

  return (
    <main className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
        <div>
          <Pill tone="olive">{guidance.title}</Pill>
          <h1 className="mt-4 text-4xl font-bold text-[#17201a]">Dashboard</h1>
          <p className="mt-3 max-w-3xl text-[#5f6958]">{guidance.copy}</p>
        </div>
        <Button onClick={() => setActivePage('upload')}>
          <UploadCloud size={18} /> New analysis
        </Button>
      </div>

      <div className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard icon={FileUp} label="Total resumes" value={dashboardData?.total_resumes ?? (uploadResult ? 1 : 0)} hint="Uploaded through the AI pipeline" tone="olive" />
        <StatCard icon={BriefcaseBusiness} label="Recommendations" value={dashboardData?.total_recommendations ?? (matches.length || 5)} hint="Ranked career matches" tone="sky" />
        <StatCard icon={Route} label="Roadmaps" value={dashboardData?.total_roadmaps ?? (uploadResult?.roadmap ? 1 : 3)} hint="Active learning paths" tone="yellow" />
        <StatCard icon={Check} label="Completed steps" value={dashboardData?.completed_steps ?? 14} hint="Progress tracked over time" tone="olive" />
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[1fr_0.9fr]">
        <section className="glass-panel rounded-lg p-5">
          <h2 className="text-xl font-bold text-[#17201a]">Skill growth radar</h2>
          <div className="mt-4 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={skillRadar}>
                <PolarGrid stroke="#dfe8d7" />
                <PolarAngleAxis dataKey="skill" tick={{ fontSize: 12, fill: '#536431' }} />
                <Radar dataKey="value" stroke="#6f7f45" fill="#8ecae6" fillOpacity={0.42} />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="glass-panel rounded-lg p-5">
          <h2 className="text-xl font-bold text-[#17201a]">Recent activity</h2>
          <div className="mt-5 grid gap-3">
            {activities.slice(0, 4).map((item, index) => (
              <div key={item} className="flex items-center gap-3 rounded-lg bg-white p-4">
                <span className="flex size-9 items-center justify-center rounded-md bg-[#e8f6fb] text-[#35708c]">
                  <Clock3 size={17} />
                </span>
                <div>
                  <p className="text-sm font-bold text-[#17201a]">{item}</p>
                  <p className="text-xs text-[#69725f]">{index + 1} step{index ? 's' : ''} ago</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  )
}

function SchoolStudentDashboard() {
  const { user } = useAppStore()
  const [answers, setAnswers] = useState({})
  const [result, setResult] = useState(null)
  const [attempts, setAttempts] = useState(
    Number(localStorage.getItem('career_quiz_attempts') || '0'),
  )

  const answeredCount = Object.keys(answers).length
  const progress = Math.round((answeredCount / quizQuestions.length) * 100)

  const submitQuiz = () => {
    const scores = Object.keys(quizProfiles).reduce((acc, category) => {
      acc[category] = 0
      return acc
    }, {})

    Object.values(answers).forEach((category) => {
      scores[category] += 1
    })

    const topScore = Math.max(...Object.values(scores))
    const topCategories = Object.entries(scores)
      .filter(([, score]) => score === topScore)
      .map(([category]) => category)

    const nextAttempts = attempts + 1
    localStorage.setItem('career_quiz_attempts', String(nextAttempts))
    setAttempts(nextAttempts)
    setResult({
      scores,
      topCategories,
    })
  }

  const resetQuiz = () => {
    setAnswers({})
    setResult(null)
  }

  return (
    <main className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
        <div>
          <Pill tone="sky">School student mode</Pill>
          <h1 className="mt-4 text-4xl font-bold text-[#17201a]">Career Exploration Quiz</h1>
          <p className="mt-3 max-w-3xl text-[#5f6958]">
            Hi {user?.first_name || 'student'}, answer honestly and discover career families that match your interests. You can attempt it multiple times.
          </p>
        </div>
        <div className="grid gap-2 rounded-lg bg-white p-4 text-sm font-semibold text-[#536431] shadow-sm">
          <span>Attempts completed: {attempts}</span>
          <span>Progress: {progress}%</span>
        </div>
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_0.8fr]">
        <section className="grid gap-4">
          {quizQuestions.map((item, questionIndex) => (
            <div key={item.question} className="metric-card rounded-lg p-5">
              <div className="flex items-start gap-3">
                <span className="flex size-9 shrink-0 items-center justify-center rounded-md bg-[#eef4e8] text-sm font-bold text-[#536431]">
                  {questionIndex + 1}
                </span>
                <div className="w-full">
                  <h2 className="text-lg font-bold leading-7 text-[#17201a]">{item.question}</h2>
                  <div className="mt-4 grid gap-3">
                    {item.options.map(([letter, option, category]) => {
                      const checked = answers[questionIndex] === category

                      return (
                        <button
                          key={`${questionIndex}-${letter}`}
                          className={classNames(
                            'rounded-lg border p-4 text-left text-sm leading-6 transition',
                            checked
                              ? 'border-[#6f7f45] bg-[#eef4e8] text-[#26341f]'
                              : 'border-[#dfe8d7] bg-white text-[#5f6958] hover:border-[#8ecae6]',
                          )}
                          onClick={() => setAnswers({ ...answers, [questionIndex]: category })}
                        >
                          <span className="font-bold">{letter})</span> {option}
                        </button>
                      )
                    })}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </section>

        <aside className="lg:sticky lg:top-24 lg:self-start">
          <div className="glass-panel rounded-lg p-5">
            <h2 className="text-xl font-bold text-[#17201a]">Quiz evaluation</h2>
            <div className="mt-4 h-3 overflow-hidden rounded-full bg-[#e8f6fb]">
              <div className="h-full rounded-full bg-[#6f7f45]" style={{ width: `${progress}%` }} />
            </div>
            <p className="mt-3 text-sm text-[#69725f]">{answeredCount} of {quizQuestions.length} questions answered.</p>
            <div className="mt-5 grid gap-3">
              <Button disabled={answeredCount !== quizQuestions.length} onClick={submitQuiz}>
                <Sparkles size={18} /> Show my career paths
              </Button>
              <Button variant="ghost" onClick={resetQuiz}>
                Attempt again
              </Button>
            </div>

            {result && (
              <div className="mt-6 grid gap-4">
                {result.topCategories.map((category) => {
                  const profile = quizProfiles[category]

                  return (
                    <div key={category} className="rounded-lg bg-white p-4">
                      <Pill tone="olive">{category}: {profile.label}</Pill>
                      <p className="mt-3 text-sm leading-6 text-[#5f6958]">{profile.description}</p>
                      <div className="mt-3 flex flex-wrap gap-2">
                        {profile.careers.map((career) => (
                          <span key={career} className="rounded-full bg-[#e8f6fb] px-3 py-1 text-xs font-semibold text-[#27556d]">
                            {career}
                          </span>
                        ))}
                      </div>
                    </div>
                  )
                })}

                <div className="rounded-lg bg-white p-4">
                  <h3 className="font-bold text-[#17201a]">Score breakdown</h3>
                  <div className="mt-3 grid gap-2">
                    {Object.entries(result.scores).map(([category, score]) => (
                      <div key={category} className="grid grid-cols-[110px_1fr_auto] items-center gap-2 text-sm">
                        <span className="font-semibold text-[#536431]">{category}</span>
                        <span className="h-2 overflow-hidden rounded-full bg-[#eef4e8]">
                          <span className="block h-full bg-[#8ecae6]" style={{ width: `${score * 10}%` }} />
                        </span>
                        <span className="font-bold text-[#17201a]">{score}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </aside>
      </div>
    </main>
  )
}

function RoadmapPage() {
  const { uploadResult } = useAppStore()
  const steps = uploadResult?.roadmap?.steps?.length
    ? uploadResult.roadmap.steps.map((step, index) => ({
        id: step.id || index + 1,
        title: step.title,
        description: step.description,
        status: index === 0 ? 'completed' : index === 1 ? 'in_progress' : 'not_started',
        completion_percentage: index === 0 ? 100 : index === 1 ? 45 : 0,
      }))
    : fallbackRoadmapSteps

  return (
    <main className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div>
        <Pill tone="sky">Interactive roadmap visualizer</Pill>
        <h1 className="mt-4 text-4xl font-bold text-[#17201a]">{uploadResult?.roadmap?.title || 'AI Engineer Roadmap'}</h1>
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-[0.85fr_1.15fr]">
        <section className="glass-panel rounded-lg p-5">
          <h2 className="text-xl font-bold text-[#17201a]">Completion progress</h2>
          <div className="mt-5 h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={steps.map((step, index) => ({ name: `Step ${index + 1}`, progress: step.completion_percentage }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e4eadf" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Line dataKey="progress" stroke="#6f7f45" strokeWidth={3} dot={{ fill: '#f4d35e', strokeWidth: 2 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="glass-panel rounded-lg p-5">
          <div className="grid gap-4">
            {steps.map((step, index) => (
              <RoadmapStep key={`${step.id}-${step.title}`} step={step} index={index} />
            ))}
          </div>
        </section>
      </div>
    </main>
  )
}

function RoadmapStep({ step, index }) {
  const status = step.status || 'not_started'
  const statusMap = {
    completed: { icon: Check, label: 'Completed', style: 'bg-[#eef4e8] text-[#536431]' },
    in_progress: { icon: Circle, label: 'In progress', style: 'bg-[#fff6c8] text-[#7a6414]' },
    not_started: { icon: Lock, label: 'Locked', style: 'bg-[#e8f6fb] text-[#35708c]' },
  }
  const StatusIcon = statusMap[status].icon

  return (
    <div className="grid gap-4 rounded-lg bg-white p-4 sm:grid-cols-[auto_1fr_auto] sm:items-center">
      <div className="flex size-11 items-center justify-center rounded-md bg-[#17201a] text-sm font-bold text-white">{index + 1}</div>
      <div>
        <h3 className="font-bold text-[#17201a]">{step.title}</h3>
        <p className="mt-1 text-sm leading-6 text-[#69725f]">{step.description || 'Build confidence through focused learning and a practical deliverable.'}</p>
      </div>
      <span className={classNames('inline-flex items-center gap-2 rounded-md px-3 py-2 text-sm font-bold', statusMap[status].style)}>
        <StatusIcon size={16} /> {statusMap[status].label}
      </span>
    </div>
  )
}

function TrendsPage() {
  return (
    <main className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <Pill tone="yellow">Static market trend engine MVP</Pill>
      <h1 className="mt-4 text-4xl font-bold text-[#17201a]">Market trends</h1>
      <p className="mt-3 max-w-3xl text-[#5f6958]">A judging-ready dataset for skill demand, job growth, and salary insight. Later this can be replaced with Adzuna, RapidAPI jobs, or stored DB trends.</p>

      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <section className="glass-panel rounded-lg p-5">
          <h2 className="text-xl font-bold text-[#17201a]">Demand visualization</h2>
          <div className="mt-5 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={marketTrends}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e4eadf" />
                <XAxis dataKey="role" tick={{ fontSize: 12 }} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="demand" fill="#8ecae6" radius={[6, 6, 0, 0]} />
                <Bar dataKey="growth" fill="#f4d35e" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="grid gap-4">
          {marketTrends.map((trend) => (
            <div key={trend.role} className="metric-card rounded-lg p-5">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <h3 className="font-bold text-[#17201a]">{trend.role}</h3>
                  <p className="mt-1 text-sm text-[#69725f]">Demand {trend.demand}% - Growth {trend.growth}%</p>
                </div>
                <Pill tone={trend.demand > 88 ? 'olive' : 'sky'}>{trend.salary} LPA</Pill>
              </div>
            </div>
          ))}
        </section>
      </div>
    </main>
  )
}

function AdminPage({ setActivePage }) {
  const { admin } = useAppStore()

  if (!admin) {
    return <AdminLoginPage setActivePage={setActivePage} />
  }

  return (
    <main className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <Pill tone="olive">Optional admin panel</Pill>
      <h1 className="mt-4 text-4xl font-bold text-[#17201a]">Admin workspace</h1>
      <p className="mt-3 max-w-3xl text-[#5f6958]">A lightweight management view for trends, skills, analytics, and learning resources.</p>

      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <AdminBlock icon={TrendingUp} title="Manage trends" items={marketTrends.map((item) => `${item.role} - ${item.demand}% demand`)} />
        <AdminBlock icon={BookOpen} title="Learning resources" items={resourceLibrary.map((item) => `${item.title} - ${item.provider}`)} />
        <AdminBlock icon={GraduationCap} title="Skill taxonomy" items={skillRadar.map((item) => `${item.skill} - ${item.value}% strength`)} />
        <AdminBlock icon={BarChart3} title="Analytics snapshot" items={['5 resumes tracked', '3 roadmaps active', '14 steps completed']} />
      </div>
    </main>
  )
}

function AdminBlock({ icon: Icon, title, items }) {
  return (
    <section className="glass-panel rounded-lg p-5">
      <div className="flex items-center gap-3">
        <span className="flex size-10 items-center justify-center rounded-md bg-[#eef4e8] text-[#536431]">
          <Icon size={20} />
        </span>
        <h2 className="text-xl font-bold text-[#17201a]">{title}</h2>
      </div>
      <div className="mt-5 grid gap-3">
        {items.map((item) => (
          <div key={item} className="rounded-lg bg-white p-4 text-sm font-semibold text-[#536431]">
            {item}
          </div>
        ))}
      </div>
    </section>
  )
}

function LearningResources() {
  return (
    <section className="mx-auto max-w-7xl px-4 pb-12 sm:px-6 lg:px-8">
      <div className="glass-panel rounded-lg p-5">
        <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
          <div>
            <Pill tone="sky">Learning resource engine</Pill>
            <h2 className="mt-3 text-2xl font-bold text-[#17201a]">Recommended learning links</h2>
          </div>
        </div>
        <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {resourceLibrary.map((resource) => (
            <div key={resource.title} className="rounded-lg bg-white p-4">
              <p className="text-xs font-bold uppercase tracking-wide text-[#8a957d]">{resource.type}</p>
              <h3 className="mt-2 font-bold text-[#17201a]">{resource.title}</h3>
              <p className="mt-2 text-sm text-[#69725f]">{resource.provider} - {resource.level}</p>
              <p className="mt-3 text-sm leading-6 text-[#5f6958]">{resource.focus}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function App() {
  const [activePage, setActivePage] = useState('landing')
  const { user, admin, studentMode } = useAppStore()
  const showResources = useMemo(
    () => !studentMode && user?.profile_type !== 'school_student' && ['dashboard', 'roadmap', 'trends', 'admin'].includes(activePage),
    [activePage, studentMode, user?.profile_type],
  )

  useEffect(() => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    })
  }, [activePage])

  const pages = {
    landing: <LandingPage setActivePage={setActivePage} />,
    'role-select': <RoleSelectPage setActivePage={setActivePage} />,
    auth: <AuthPage setActivePage={setActivePage} />,
    'admin-login': <AdminLoginPage setActivePage={setActivePage} />,
    upload: <UploadPage setActivePage={setActivePage} />,
    results: <ResultsPage />,
    dashboard: <DashboardPage setActivePage={setActivePage} />,
    'student-dashboard': <SchoolStudentDashboard />,
    roadmap: <RoadmapPage />,
    trends: <TrendsPage />,
    admin: <AdminPage setActivePage={setActivePage} />,
  }

  return (
    <div>
      <Header activePage={activePage} setActivePage={setActivePage} />
      {pages[activePage]}
      {showResources && <LearningResources />}
      <footer className="border-t border-[#dfe8d7] px-4 py-6 text-center text-sm font-medium text-[#69725f]">
        {admin ? 'CareerPilot AI Admin' : 'CareerPilot AI'} - FastAPI, React, Tailwind, Recharts, Zustand, JWT
      </footer>
    </div>
  )
}

export default App
