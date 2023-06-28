import {createRouter, createWebHistory} from 'vue-router'

import Login from "./views/beforeHome/Login.vue"
import Home from "./views/Home.vue"
import Top from "./views/Top.vue"
import Sign from "./views/beforeHome/Sign.vue"
import UserShow from "@/components/userCenter/UserShow.vue";
import DetailsCheck from "@/components/userCenter/DetailsCheck.vue";
import PwdChange from "@/components/userCenter/PwdChange.vue";
import Manage from "@/views/Manage.vue";
import Train from "@/views/Train.vue";
import Infer from "@/views/Infer.vue";
import CaseShow from "@/components/caseManage/CaseShow.vue";
import CaseCreate from "@/components/caseManage/CaseCreate.vue";
import HelpAbout from "@/components/caseManage/HelpAbout.vue";


const routes = [
    {path: '/', component: Top},
    {path: '/login', component: Login},
    {path: '/sign', component: Sign},
    {
        path: '/home', component: Home, children: [
            {path: '/home/show', component: UserShow},
            {path: '/home/details', component: DetailsCheck},
            {path: '/home/pwd', component: PwdChange},
        ]
    },
    {
        path: '/manage', component: Manage, children: [
            {path: '/manage/show', component: CaseShow},
            {path: '/manage/create', component: CaseCreate},
            {path: '/manage/ha', component: HelpAbout},
        ]
    },
    {path: '/train', component: Train},
    {path: '/infer', component: Infer},

];

const router = createRouter({
    history: createWebHistory(),
    routes
});
export default router
