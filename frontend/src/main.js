import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 引入Vant
import { 
  Button, 
  Cell, 
  CellGroup, 
  Field, 
  Form, 
  NavBar, 
  Tabbar, 
  TabbarItem,
  Calendar,
  Picker,
  Popup,
  DatePicker,
  Dialog,
  Toast,
  Loading,
  Icon,
  Empty,
  Uploader,
  Card,
  Tag,
  Steps,
  Step
} from 'vant'

// 引入Vant样式
import 'vant/lib/index.css'

// 导入全局样式
import './assets/main.css'

// 导入dayjs
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'

// 设置dayjs语言为中文
dayjs.locale('zh-cn')

// 创建Vue应用
const app = createApp(App)

// 使用插件
app.use(createPinia())
app.use(router)

// 注册Vant组件
app.use(Button)
app.use(Cell)
app.use(CellGroup)
app.use(Field)
app.use(Form)
app.use(NavBar)
app.use(Tabbar)
app.use(TabbarItem)
app.use(Calendar)
app.use(Picker)
app.use(Popup)
app.use(DatePicker)
app.use(Dialog)
app.use(Toast)
app.use(Loading)
app.use(Icon)
app.use(Empty)
app.use(Uploader)
app.use(Card)
app.use(Tag)
app.use(Steps)
app.use(Step)

// 挂载应用
app.mount('#app') 