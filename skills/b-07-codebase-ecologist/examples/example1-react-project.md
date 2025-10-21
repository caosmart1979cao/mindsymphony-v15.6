# 示例 1：分析 React 电商项目

## 用户请求

```
召唤 [B-07] 代码库生态学家，
帮我理解这个 React 电商项目的代码结构
项目路径：/projects/ecommerce-app
```

## 代码库生态学家输出

---

# React 电商项目 - 代码库分析报告

## 项目概览

**技术栈**：
- 前端框架：React 18.2.0
- 状态管理：Redux Toolkit
- 路由：React Router v6
- UI 库：Material-UI (MUI)
- 构建工具：Vite

**项目规模**：
- 总文件数：156 个
- 代码行数：~12,000 行
- 核心模块：8 个

## 目录结构分析

```
ecommerce-app/
├── src/
│   ├── components/        [32 个组件] - UI 组件库
│   ├── pages/            [8 个页面] - 路由页面
│   ├── features/         [6 个功能模块] - 业务逻辑
│   │   ├── auth/        ⭐ 认证模块
│   │   ├── cart/        ⭐ 购物车模块
│   │   ├── products/    ⭐ 商品模块
│   │   ├── orders/      ⭐ 订单模块
│   │   ├── user/        ⭐ 用户模块
│   │   └── payment/     ⭐ 支付模块
│   ├── store/           [Redux 配置]
│   ├── hooks/           [12 个自定义 Hooks]
│   ├── utils/           [工具函数]
│   └── api/             [API 调用层]
```

## 核心依赖关系图

```
App.js
 ├─→ Router 配置
 │    ├─→ HomePage
 │    ├─→ ProductListPage → ProductCard 组件
 │    ├─→ ProductDetailPage → AddToCart 功能
 │    ├─→ CartPage → Cart 功能模块 🔥
 │    ├─→ CheckoutPage → Payment 功能模块
 │    └─→ OrderHistoryPage → Orders 功能模块
 │
 └─→ Redux Store
      ├─→ authSlice (认证状态)
      ├─→ cartSlice (购物车状态) 🔥
      ├─→ productsSlice (商品状态)
      └─→ ordersSlice (订单状态)
```

🔥 = 高频修改/核心模块

## 关键发现

### 1. 热点模块（频繁被引用）

**cartSlice.js** - 被 18 个文件引用
- 直接引用：Cart.js, CartPage.js, ProductDetail.js
- 通过 useCart hook 引用：15 个组件

**authSlice.js** - 被 23 个文件引用
- 几乎所有需要权限控制的组件都依赖它

**ProductCard.js** - 被 6 个页面/组件重用
- 是最常用的展示组件

### 2. 代码质量评估

**优点**：
- ✅ 模块划分清晰，职责单一
- ✅ 使用 Redux Toolkit 减少样板代码
- ✅ 自定义 Hooks 复用良好

**技术债**：
- ⚠️ 部分组件过大（CartPage.js 450 行）
- ⚠️ API 调用分散在多个文件中，缺乏统一管理
- ⚠️ 缺少单元测试

### 3. Git 历史洞察

**最近变更（过去 30 天）**：
- cart/ 模块：15 次提交（功能迭代频繁）
- payment/ 模块：8 次提交（新增支付方式）
- auth/ 模块：3 次提交（修复 bug）

**历史问题**：
- 购物车相关 bug 修复记录较多（7 次）
- 建议重点关注购物车逻辑的稳定性

## 重要函数调用分析

### calculateTotal() 函数

**位置**：`src/utils/cart.js:42`

**被调用处**（5 处）：
1. `CartPage.js:78` - 购物车总价显示
2. `CheckoutPage.js:156` - 结账页总价
3. `OrderSummary.js:23` - 订单摘要
4. `useCart.js:34` - 自定义 Hook 内部
5. `cartSlice.js:89` - Redux reducer 中计算

**影响范围**：
- 🔴 高风险：修改会影响所有订单计算逻辑
- 建议：修改前务必编写测试用例

### authenticateUser() 函数

**位置**：`src/features/auth/authService.js:12`

**调用链**：
```
LoginPage
 └─→ useAuth hook
      └─→ dispatch(loginUser())
           └─→ authSlice thunk
                └─→ authenticateUser()
                     └─→ API: POST /auth/login
```

## 重构建议

### 优先级 1：高风险但价值高

1. **抽取 API 调用层**
   - 当前问题：API 调用分散在各功能模块
   - 建议：创建统一的 `api/services/` 目录
   - 影响文件：~20 个
   - 风险：中等（需要重新测试）

2. **拆分大型组件**
   - 目标：CartPage.js (450 行)
   - 建议：拆分为 CartList + CartSummary + CartActions
   - 影响文件：1 个
   - 风险：低

### 优先级 2：提升代码质量

1. **增加单元测试**
   - 优先覆盖：cart 和 payment 模块
   - 目标覆盖率：>60%

2. **优化状态管理**
   - 考虑使用 RTK Query 替代手写 API 调用
   - 减少样板代码

## 下一步行动建议

如果你想：
- **理解某个具体功能** → 告诉我功能名称，我详细分析
- **重构某个模块** → 我帮你分析影响范围和重构路径
- **查找特定代码** → 告诉我要找什么，我精准定位
- **开始重构** → 召唤 [B-08] 智能重构师继续

---

**代码地图已绘制完成 | [B-07] 代码库生态学家**
