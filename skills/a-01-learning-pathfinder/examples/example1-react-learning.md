# 示例 1：React 学习路径设计

## 用户请求

```
召唤 [A-01] 路径点灯人，我想学习 React，
目前会 HTML/CSS 和基础 JavaScript（变量、函数、循环），
目标是能独立开发中小型 Web 应用。
```

## 路径点灯人输出

---

# React 开发 - 学习路径

## 学习目标

**最终能力**：
- 独立开发中小型 React Web 应用
- 理解 React 核心概念和最佳实践
- 能够使用现代 React 生态系统工具
- 具备调试和性能优化能力

## 当前评估

**你的起点**：
- ✅ HTML/CSS 基础
- ✅ JavaScript 基础（变量、函数、循环）
- ⚠️ 需要补充：ES6+ 特性、异步编程

**时间投入**：
- 总时长：10-12 周（每天 2 小时）
- 快速路径：6-8 周（每天 3-4 小时）

**难度评级**：★★★☆☆（中等，适合有编程基础者）

---

## 学习路径

### 阶段 0：JavaScript 进阶准备（2 周）

**目标**：补足学习 React 所需的现代 JavaScript 知识

**核心能力**：
- 掌握 ES6+ 语法（箭头函数、解构、模板字符串等）
- 理解异步编程（Promise、async/await）
- 熟悉数组方法（map、filter、reduce）

**学习内容**：
1. **ES6 核心特性** | 资源：MDN Web Docs - ES6 教程
   - let/const、箭头函数、解构赋值
   - 模板字符串、默认参数
   - 展开运算符 (...) 和剩余参数

2. **异步 JavaScript** | 资源：JavaScript.info - Promises
   - 回调函数的问题
   - Promise 基础和链式调用
   - async/await 语法

3. **函数式编程基础** | 资源：freeCodeCamp
   - 数组的 map、filter、reduce
   - 函数作为参数
   - 不可变数据概念

**实践项目**：
📝 **Todo List（纯 JS 版）** - 用 ES6+ 语法实现
- 添加/删除/标记完成任务
- 使用数组方法管理数据
- 练习事件处理和 DOM 操作

**验收标准**：
- [ ] 能熟练使用箭头函数和解构
- [ ] 理解 Promise 和 async/await
- [ ] 能用 map/filter/reduce 处理数组数据
- [ ] 完成 Todo List 项目

---

### 阶段 1：React 基础（2 周）

**目标**：理解 React 核心概念，能创建简单组件

**核心能力**：
- 理解组件化思想
- 掌握 JSX 语法
- 使用 Props 传递数据
- 管理组件 State

**学习内容**：
1. **React 入门** | 资源：React 官方文档 - Quick Start
   - 什么是组件
   - JSX 语法规则
   - 用 Vite 创建第一个 React 项目

2. **Props 和组件组合** | 资源：React 官方教程
   - Props 的传递和接收
   - 组件的嵌套和复用
   - Children prop

3. **State 和事件处理** | 资源：React 文档 - State
   - useState Hook 基础
   - 事件处理（onClick、onChange 等）
   - 更新 State 的正确方式

**实践项目**：
🎨 **简单计数器 App**
- 显示数字，有增加/减少按钮
- 可以设置步长（Props）
- 多个计数器组件复用

📝 **Todo List（React 版）**
- 用组件重构之前的 Todo List
- 拆分为 TodoList、TodoItem 组件
- 使用 State 管理任务列表

**验收标准**：
- [ ] 能独立创建 React 组件
- [ ] 理解 Props 和 State 的区别
- [ ] 能处理基本的用户交互
- [ ] 完成两个实践项目

---

### 阶段 2：React Hooks 深入（2 周）

**目标**：掌握常用 Hooks，处理副作用和复杂状态

**核心能力**：
- 使用 useEffect 处理副作用
- 用 useContext 共享状态
- 理解 Hook 规则
- 创建自定义 Hook

**学习内容**：
1. **useEffect 和副作用** | 资源：React 文档 - useEffect
   - 组件生命周期概念
   - 数据获取（API 调用）
   - 清理副作用

2. **更多 Hooks** | 资源：React Hooks 文档
   - useContext：跨组件传递数据
   - useReducer：复杂状态管理
   - useMemo/useCallback：性能优化

3. **自定义 Hook** | 资源：React 自定义 Hook 指南
   - 提取可复用逻辑
   - 常见自定义 Hook 模式

**实践项目**：
🌐 **电影搜索 App**
- 调用 OMDB API 搜索电影
- 使用 useEffect 获取数据
- 显示加载状态和错误处理
- 创建 useFetch 自定义 Hook

**验收标准**：
- [ ] 能用 useEffect 处理 API 调用
- [ ] 理解 useContext 的使用场景
- [ ] 能创建简单的自定义 Hook
- [ ] 完成电影搜索项目

---

### 阶段 3：路由和状态管理（2 周）

**目标**：构建多页面应用，管理全局状态

**核心能力**：
- 使用 React Router 实现路由
- 理解全局状态管理
- 掌握 Redux Toolkit 基础
- 异步状态管理

**学习内容**：
1. **React Router** | 资源：React Router 官方文档
   - 基础路由配置
   - 嵌套路由和动态路由
   - 路由参数和导航

2. **Redux Toolkit** | 资源：Redux Toolkit 官方教程
   - 为什么需要全局状态
   - Store、Slice、Reducer 概念
   - 使用 createSlice 和 configureStore

3. **异步 Redux** | 资源：RTK Query 文档
   - createAsyncThunk
   - RTK Query 基础
   - 缓存和数据同步

**实践项目**：
🛒 **简易电商前端**
- 多个页面（首页、商品列表、商品详情、购物车）
- 使用 React Router 实现路由
- 用 Redux 管理购物车状态
- 用 RTK Query 获取商品数据

**验收标准**：
- [ ] 能配置多页面路由
- [ ] 理解 Redux 的工作原理
- [ ] 能使用 Redux Toolkit 管理状态
- [ ] 完成电商前端项目

---

### 阶段 4：实战项目和进阶（2-4 周）

**目标**：综合运用所学，完成完整项目

**核心能力**：
- 项目架构和文件组织
- 样式解决方案（CSS Modules / Styled Components）
- 表单处理和验证
- 测试基础

**学习内容**：
1. **项目结构最佳实践** | 资源：React 项目结构指南
   - 文件夹组织方式
   - 组件分类（pages/components/features）
   - 配置管理

2. **样式方案** | 资源：根据兴趣选择
   - CSS Modules
   - Styled Components
   - TailwindCSS + React

3. **表单处理** | 资源：React Hook Form 文档
   - 受控 vs 非受控组件
   - 表单验证
   - React Hook Form 库

4. **测试入门** | 资源：React Testing Library
   - 组件测试基础
   - 测试用户交互
   - Mock API 调用

**实战项目（选一个）**：

**选项 A：个人博客系统**
- 文章列表、详情、分类、标签
- Markdown 编辑器
- 评论功能
- 暗黑模式切换

**选项 B：任务管理看板**
- 看板视图（待办/进行中/已完成）
- 拖拽排序
- 任务筛选和搜索
- 数据持久化

**选项 C：社交媒体 Feed**
- 帖子 Feed 流
- 点赞/评论/分享
- 用户资料页
- 实时更新（可选）

**验收标准**：
- [ ] 项目结构清晰，代码组织良好
- [ ] 至少使用 3-4 个第三方库
- [ ] 有基本的错误处理和加载状态
- [ ] 完成一个完整的实战项目
- [ ] 能部署到 Vercel/Netlify

---

## 学习策略建议

### 每日学习计划（每天 2 小时）

**第 1 小时**：理论学习
- 阅读文档/教程（30分钟）
- 看视频/示例代码（30分钟）

**第 2 小时**：动手实践
- 跟着教程敲代码（30分钟）
- 独立完成小练习（30分钟）

**每周末**：项目实践（4 小时）
- 完成阶段性项目
- 复习本周内容

### 常见陷阱及应对

❌ **陷阱 1：只看不练**
→ 应对：每学一个概念，立即写代码验证

❌ **陷阱 2：完美主义**
→ 应对：先跑通，再优化。丑陋的能跑的代码 > 完美的空想

❌ **陷阱 3：跳跃式学习**
→ 应对：严格按路径走，不要提前学 Redux（容易挫败）

❌ **陷阱 4：孤立学习**
→ 应对：加入社区（React 中文社区、Discord），提问和分享

❌ **陷阱 5：堆砌教程**
→ 应对：选定一个教程深入学完，而非同时看 10 个

### 学习资源推荐

**免费资源**：
1. React 官方文档（必读，质量最高）
2. freeCodeCamp React 课程
3. Scrimba React 互动教程
4. YouTube - Traversy Media、Net Ninja

**付费资源（可选）**：
1. Udemy - React Complete Guide（中文/英文）
2. Frontend Masters - Complete Intro to React

**实践平台**：
1. CodeSandbox（在线编辑器）
2. StackBlitz（在线 IDE）

## 进阶路线

完成此路径后，根据兴趣可继续学习：

**前端深化方向**：
- Next.js（React 全栈框架）
- TypeScript + React
- React Native（移动开发）
- 前端性能优化

**全栈方向**：
- Node.js + Express
- GraphQL + React
- 数据库（MongoDB/PostgreSQL）
- 身份认证（JWT、OAuth）

**工程化方向**：
- Webpack/Vite 深入
- 前端测试（Jest、Cypress）
- CI/CD 部署
- Monorepo 管理

---

## 给你的鼓励

React 学习曲线确实存在，但：
- 前 2 周最难（新概念多），坚持过去就顺了
- 第一个能跑的项目会带来巨大成就感
- 3 个月后回看，会惊讶于自己的进步

**记住**：
> "每个 React 高手都曾搞不懂 Props 和 State 的区别"

你已经有了编程基础，这个路径为你量身定制。
**从明天开始，阶段 0 见！** 🚀

---

**愿这条路径，点亮你的前端之旅 | [A-01] 路径点灯人**
