//导入vue-router
import { createRouter, createWebHistory } from 'vue-router'
//导入组件
import LoginVue from '@/views/Login.vue'
import LayoutVue from '@/layout/Layout.vue'
import ConversationVue from '@/views/conversation.vue'
import ProjcetVue from '@/views/project.vue'
import DatasetVue from '@/views/tool/dataset.vue'
import EntityVue from '@/views/tool/entity.vue'
import PictureVue from '@/views/tool/picture.vue'
import TableVue from '@/views/tool/table.vue'
import ChatVue from '@/views//ChatView.vue'


import DocumentLibrary from '../views/DocumentLibrary.vue'

//定义路由关系
const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: LoginVue },
    {
        path: '/main',
        component: LayoutVue,
        children: [
            { path: '/conversation', name:'conversation', component: ConversationVue },
            { path: '/chat', name: 'chat', component: ChatVue, },
            { path: '/project', name: 'ProjcetVue', component: ProjcetVue },
            { path: '/tool/dataset', component: DatasetVue },
            { path: '/tool/entity', name: 'EntityVue', component: EntityVue },
            { path: '/tool/picture', name: 'PictureVue', component: PictureVue },
            { path: '/tool/table', name: 'TableVue', component: TableVue },
            {
                path: '/documents',
                name: 'DocumentLibrary',
                component: DocumentLibrary
            },
        ]
    }
]

//创建路由器
const router = createRouter({
    history: createWebHistory(),
    routes: routes
});

export default router