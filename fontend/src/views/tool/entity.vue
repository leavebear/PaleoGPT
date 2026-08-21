
<template>
  <div class="common-layout" style="margin: 0%;">
    <el-container style="height: 82vh;">
      <el-header style="height: 130px; display: flex; align-items: center; 
      justify-content: flex-start; 
      flex-wrap: wrap;
      ">

        <div style="width: 100%; padding: 0%; display: flex;">
          <!-- <el-text style="font-weight: bold; padding-right: 10px;" >文件选择</el-text> -->
           <div class="header">
          <span class="title">实体关系抽取
      <svg t="1740116777201" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1436" width="28" height="28"><path d="M754.752 587.968h139.904L896 494.208l-101.312-115.84h-39.936v209.6z" fill="#1296db" p-id="1437"></path><path d="M404.48 177.6a17.088 17.088 0 0 0-13.056 6.08L177.6 437.376V832c0 9.408 7.68 17.088 17.088 17.088h544c9.408 0 17.024-7.68 17.024-17.088V194.688a17.088 17.088 0 0 0-17.024-17.088H404.48z m-52.16-26.88c12.928-15.424 32-24.32 52.16-24.32h334.208c37.696 0 68.224 30.592 68.224 68.288V832c0 37.76-30.528 68.288-68.224 68.288h-544c-37.76 0-68.288-30.592-68.288-68.288V418.624l225.92-267.968z" fill="#1296db" p-id="1438"></path><path d="M405.376 493.312a64 64 0 0 0-64 64v170.688a64 64 0 0 0 64 64H832a64 64 0 0 0 64-64V493.312H405.376z m66.432 54.4c-27.136 0-48.64 9.216-64.512 28.16-15.104 17.664-22.528 40.192-22.528 67.584 0 27.136 7.424 49.408 22.528 66.56 16.128 18.432 38.656 27.648 67.84 27.648 16.384 0 30.976-2.048 44.288-6.144a120.32 120.32 0 0 0 11.648-4.48c14.592-6.464 21.632-22.272 21.632-38.208v-12.864a39.168 39.168 0 0 0-39.168-39.168h-26.368a12.8 12.8 0 0 0 0 25.6h11.648c13.248 0 23.936 10.688 23.936 23.872 0 8.512-4.48 16.64-12.352 19.712a83.072 83.072 0 0 1-32 5.568c-22.208 0-38.592-6.144-49.088-18.432-9.728-11.52-14.592-28.16-14.592-49.664 0-22.528 5.376-39.68 16.384-51.968 9.984-11.776 23.552-17.408 40.704-17.408 13.824 0 25.088 2.816 33.536 8.704a39.232 39.232 0 0 1 12.416 14.72c3.2 6.4 9.088 11.648 16.256 11.648 9.344 0 16.64-8.512 13.44-17.344a62.528 62.528 0 0 0-20.096-28.48c-13.568-10.496-32-15.616-55.552-15.616z m131.264 0a19.712 19.712 0 0 0-14.08 5.376 17.92 17.92 0 0 0-5.632 13.824c0 5.632 1.792 10.24 5.632 14.08 3.84 3.584 8.448 5.376 14.08 5.376s10.24-1.792 14.08-5.376a18.752 18.752 0 0 0 5.888-14.08 18.88 18.88 0 0 0-5.632-13.824 20.352 20.352 0 0 0-14.336-5.376z m0 54.016a14.592 14.592 0 0 0-14.592 14.592v103.168a14.592 14.592 0 1 0 29.184 0V616.32a14.592 14.592 0 0 0-14.592-14.592z m75.648-40.704c6.144-6.656 15.36-9.728 27.136-9.728h15.872a12.288 12.288 0 1 1 0 24.576h-11.776c-3.84 0-6.656 1.024-8.704 3.072-2.048 2.048-2.816 5.12-2.816 9.472v6.528c0 3.712 3.008 6.784 6.72 6.784h15.168a11.904 11.904 0 0 1 0 23.808h-15.168a6.784 6.784 0 0 0-6.72 6.72v87.232a14.592 14.592 0 1 1-29.184 0V631.424a5.888 5.888 0 0 0-5.888-5.888h-11.648a11.904 11.904 0 0 1 0-23.808h11.648c3.2 0 5.888-2.688 5.888-5.888v-8.192c0-11.264 3.072-20.224 9.472-26.624z" fill="#1296db" p-id="1439"></path><path d="M404.672 406.72V197.824a32 32 0 0 0-56.192-20.864L167.808 385.728A32 32 0 0 0 192 438.656h180.672a32 32 0 0 0 32-31.936z" fill="#1296db" p-id="1440"></path></svg></span>
      <div class="search-container">
          <el-select
            v-model="value"
            placeholder="文件选择" 
          class="pdf-select"
          size="large"
          style="width:80%;"
          >
           <template #prefix>
        <svg t="1740117903957" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2296" width="32" height="32">
          <path d="M762.794667 702.805333A373.376 373.376 0 0 0 205.312 208 373.333333 373.333333 0 0 0 702.72 763.392l120.106667 120.106667a42.666667 42.666667 0 0 0 60.330666-60.330667l-120.362666-120.362667z m-215.04-409.898666a184.832 184.832 0 0 0-69.12-13.312 25.6 25.6 0 0 1-0.042667-51.2 234.965333 234.965333 0 0 1 166.997333 69.034666 235.434667 235.434667 0 0 1 65.28 208.64 25.6 25.6 0 0 1-50.432-9.088 184.277333 184.277333 0 0 0-51.072-163.328 183.808 183.808 0 0 0-61.568-40.746666z" fill="#1296db" p-id="2297"></path>
        </svg>
        </template>
            <el-option
              class="option"
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select> 
          </div>
          </div>
        </div>

        <!-- 清空标记按钮，只有在 textList 中至少有一个文本项有标签时才可点击 -->
        <div style="width: 100%;">
          <el-button
              size="large"
              :disabled="!textList.some(item => item.text_tag.length > 0)" 
              ghost
              @click="handleAllDelete" 
            >
              清空标记
          </el-button>

        <!-- 按钮组：返回和保存 -->
          <el-button-group>
            <el-button size="large" @click="back">返回</el-button>
            <el-button size="large" @click="handleSave">保存</el-button>
            <el-button size="large" @click="toggleRelations">显示</el-button>
            
          </el-button-group>
        </div>

      </el-header>

      <el-main style="padding-top: 0%;  overflow-y: auto;">
        <el-container style="height: 100%;display: flex;">
          <el-aside style="flex: 7.5; height: 100%; overflow-y: auto;" >
            <div id="text-container" class="text" @mouseup="handleTextSelect" style="position: relative;">
              <div class="text-wrapper">
                <div v-html="renderedText"></div>
              </div>
            </div>
          </el-aside>

          <el-main class="information-box" style="flex: 2.3; margin-left: 10px;height: 100%; overflow-y: auto;">
            <!-- 标签选择 -->
            <div
              v-if="tagInfo.visible && tagList.length > 0"
              :class="['tag-box p-4 ']"
              :style="{ top: tagInfo.top + 'px', left: tagInfo.left + 'px' }"
            >
              <div
                v-for="i in tagList"
                :key="i.tag_id"
                class="tag-name"
                @click="handleSelectLabel(i)"  
              >
                <n-space>
                  <p>{{ i.tag_name }}</p>
                  <n-button v-if="i.tag_id == editTag.tag_id" text type="primary">√</n-button>
                </n-space>
                <div :class="['w-4 h-4']" :style="{ background: i.tag_color }"></div>
              </div>
            </div>

            <!-- 重选/取消 -->
            <div
              v-if="editTag.visible"
              class="edit-tag"
              :style="{ top: editTag.top + 'px', left: editTag.left + 'px' }"
            >
              <div class="py-1 bg-gray-100 text-center">{{ editTag.tag_name || '未选择标签' }}</div>
              
              <!-- 取消按钮，关闭编辑框 -->
              <div class="py-1 bg-gray-100 text-center" @click="handleCancel">取消</div>
              <!-- 重选按钮，重置标签 
              <div class="py-1 bg-gray-100 mt-2 text-center" @click="handleReset">重选</div> -->
            </div>

            <!-- 颜色块容器 -->
            <div class="color-block-container">
              <div
                v-for="(tag, index) in tagList"
                :key="index"
                class="color-block"
                :style="{ backgroundColor: tag.tag_color }"
              >
                {{ tag.tag_name }}
              </div>
            </div>
            <!-- 分隔线 -->
<hr class="separator">

          <!-- 关系类型框 -->
<div class="relationship-block-container">
  <div
    v-for="(relation, index) in relationList"
    :key="index"
    class="relationship-block"
    @dblclick="filterRelation(relation)"
    @click="clearRelationFilter"
  >
    <div class="entity-block" :style="{ backgroundColor: relation.entity1_color }">
      {{ relation.entity1_name }}
    </div>
    <div class="relation-line" :style="{ color: relation.relation_color }">-></div>
    <div class="entity-block" :style="{ backgroundColor: relation.entity2_color }">
      {{ relation.entity2_name }}
    </div>
  </div>
  <div v-if="filterState.isFiltered" class="relationship-filter-hint">
    当前筛选: {{ filterState.activeRelation?.entity1_name }} → {{ filterState.activeRelation?.entity2_name }} (单击任意处取消筛选)
  </div>
</div>
</el-main>
          
        </el-container>
      </el-main>

      <el-footer style="display: flex; justify-content: flex-end;">
        <el-button type="success" plain>数据导出</el-button>
        
      </el-footer>
    </el-container>
  </div>
</template>


  
<script setup lang="ts">
import { ref, reactive, computed ,onMounted,onUnmounted} from 'vue';
import { useRouter } from 'vue-router';
import { getMarkContentDataService,updateMarkContentDataService } from '../../api/entity.js';
import { ElMessageBox, ElMessage } from 'element-plus';
// 添加全局函数声明
declare global {
  interface Window {
    handleEntityClick: (event: MouseEvent, tag: TSelectText) => void;
  }
}
// 然后在组件setup中定义这个函数
window.handleEntityClick = (event, tag) => {
  handleTagClick(tag, event);
};

type TTag = {
  tag_name: string;
  tag_id: string;
  tag_color: string;
};

type TSelectText = {
  tag_id: string;
  start: number;
  end: number;
  mark_content: string;
  text_id: string;  // 添加这一行
};

type TMarkContent = {
  text: string;      // 当前段落的文本内容
  text_tag: TSelectText[];
};

type TTextList = TMarkContent[];
type TTagList = TTag[];

type TRelation = {
  entity1_name: string;
  entity1_color: string;
  entity2_name: string;
  entity2_color: string;
  relation_color: string; // 关系线的颜色
};

const filterState = reactive({
  activeRelation: null as null | TRelation,
  activeEntity: null as null | {
    text_id: string;
    start: number;
    end: number;
    tag_id: string;
  },
  isFiltered: false
});

// 添加状态控制关系线的显示
const showRelations = ref(true);

// 切换关系线显示状态的方法
const toggleRelations = () => {
  showRelations.value = !showRelations.value;
  updateRelationLines();
};

// 筛选特定关系
const filterRelation = (relation: TRelation) => {
  filterState.activeRelation = relation;
  filterState.isFiltered = true;
  updateRelationLines();
};

const filterRelationsByEntity = (tag: TSelectText) => {
  // 如果点击的是当前已筛选的实体，则取消筛选
  if (filterState.activeEntity && 
      filterState.activeEntity.text_id === tag.text_id &&
      filterState.activeEntity.start === tag.start &&
      filterState.activeEntity.end === tag.end) {
    filterState.activeEntity = null;
    filterState.isFiltered = false;
  } else {
    // 否则设置新的筛选实体
    filterState.activeEntity = {
      text_id: tag.text_id,
      start: tag.start,
      end: tag.end,
      tag_id: tag.tag_id
    };
    filterState.isFiltered = true;
  }
  
  updateRelationLines();
};

// 清除筛选（单击时清除）
const clearRelationFilter = () => {
  if (filterState.activeRelation) {
    filterState.activeRelation = null;
    filterState.isFiltered = false;
    updateRelationLines();
  }
};

// 添加关系线相关的状态
const relationState = reactive({
  firstEntity: null as null | {
    text_id: string;
    start: number;
    end: number;
    tag_id: string;
    element: HTMLElement; // 保存DOM元素引用
  },
  secondEntity: null as null | {
    text_id: string;
    start: number;
    end: number;
    tag_id: string;
    element: HTMLElement;
  },
  relations: [] as Array<{
    from: { text_id: string; start: number; end: number };
    to: { text_id: string; start: number; end: number };
    relation: TRelation;
  }>,
});

const relationList = ref<TRelation[]>([
 
  {
    entity1_name: "LOC",
    entity1_color: "#C68369", // LOC 的颜色
    entity2_name: "FACE",
    entity2_color: "#DB8856", // FOS 的颜色
    relation_color: "#00BFFF", // 关系线的颜色
  },
   {
    entity1_name: "SAMPLE",
    entity1_color: "#BB01CF", // SAMPLE 的颜色
    entity2_name: "Time",
    entity2_color: "#969F04", // TIME 的颜色
    relation_color: "#FFD700", // 关系线的颜色
  },
  // 可以根据需要添加更多关系类型
]);


const textList = ref<TTextList>([
  // {
  //   text: "Shallowing of the reef crest is also indicated by the presence of the shallow-water benthic Foraminifera Baculogypsina sphaerulata tests after 2000 yr BP.",
  //   text_tag: [
  //     // {
  //     //   tag_id: "tag_id1",
  //     //   start: 8,
  //     //   end: 12,
  //     //   mark_content: "数据分析"
  //     // },
  //     // {
  //     //   tag_id: "tag_id2",
  //     //   start: 4,
  //     //   end: 6,
  //     //   mark_content: "应用"
  //     // }
  //   ]
  // },
  // {
  //   text: " The relative sea-level fall also caused subaerial exposure of the reef crest during low tides and the transition of reef-building organisms from corals to shallowwater species of benthic Foraminifera, resulting in a change noticeable in the constituents of backreef sediments.",
  //   text_tag: [
  //     // {
  //     //   tag_id: "tag_id1",
  //     //   start: 8,
  //     //   end: 12,
  //     //   mark_content: "数据分析"
  //     // },
  //     // {
  //     //   tag_id: "tag_id2",
  //     //   start: 4,
  //     //   end: 6,
  //     //   mark_content: "应用"
  //     // }
  //   ]
  // },
  // {
  //   text: "The reef flat is the most conspicuous feature of modern coral reefs, with its shallow depth and high abundance of reef organisms.",
  //   text_tag: [
  //     // {
  //     //   tag_id: "tag_id1",
  //     //   start: 8,
  //     //   end: 12,
  //     //   mark_content: "数据分析"
  //     // },
  //     // {
  //     //   tag_id: "tag_id2",
  //     //   start: 4,
  //     //   end: 6,
  //     //   mark_content: "应用"
  //     // }
  //   ]
  // },
  // // {
  // //   text: "机器学习是人工智能的重要分支。",
  // //   text_tag: [
  // //     {
  // //       tag_id: "tag_id3",
  // //       start: 0,
  // //       end: 4,
  // //       mark_content: "机器学习"
  // //     },
  // //     {
  // //       tag_id: "tag_id4",
  // //       start: 5,
  // //       end: 9,
  // //       mark_content: "人工智能"
  // //     }
  // //   ]
  // // }
])

const tagList = ref<TTagList>([
  // {
  //   tag_name: "FACE",
  //   tag_color: "#FF5733FF",
  //   tag_id: "tag_id1"
  // },
  // {
  //   tag_name: "LOC",
  //   tag_color: "#33FF57FF",
  //   tag_id: "tag_id2"
  // },
  // {
  //   tag_name: "FOS",
  //   tag_color: "#FF33A6FF",
  //   tag_id: "tag_id3"
  // },
  // {
  //   tag_name: "Time",
  //   tag_color: "#F666A6F0",
  //   tag_id: "tag_id4"
  // },
  // {
  //   tag_name: "STR",
  //   tag_color: "#B533FFFF",
  //   tag_id: "tag_id5"
  // }
])

const TAG_WIDTH = 280;

//标签选择框的可见和位置信息
const tagInfo = ref({
  visible: false,
  top: 0,
  left: 0,
});

//目前还不知道是什么框框
const editTag = ref({
  visible: false,
  top: 0,
  left: 0,
  mark_id: '',
  content: '',
  tag_id: '',
  start: 0,
  end: 0,
  tag_name: '',
});


const pdf_id =123;
const router = useRouter();


//前端进行实体标记需要用到的临时的实体标注
const selectedText = reactive({
  start: 0,
  end: 0,
  content: '',
  text_id:  ''
});


//获取数据接口 调试成功
onMounted(() => {
  getMarkContentDataService(pdf_id)
    .then(response => {
      console.log("Received data:", response); // 打印数据来检查
      if (response.status_code === 0) {
        
        const data = response.data;
        console.log("Received data:", data);
        const textListData: TTextList = data.textList.map((textItem: { text: string, text_tag: Array<any> }) => {
          const text_tag: TSelectText[] = textItem.text_tag.map((tagItem: { tag_id: string, start: number, end: number, mark_content: string }) => ({
            tag_id: tagItem.tag_id,
            start: tagItem.start,
            end: tagItem.end,
            mark_content: tagItem.mark_content
          }));

          return {
            text: textItem.text,
            text_tag
          };
        });

        // 更新 textList
textList.value = textListData;

// 处理 tagList
const tagListData: TTagList = [];
const uniqueTags: Record<string, boolean> = {}; // 用于记录已经处理过的实体类型名和颜色

data.ttag.forEach((tagItem: { tag_name: string; tag_color: string; tag_id: string }) => {
  // 创建一个唯一的标识符，用于判断是否重复
  const tagKey = `${tagItem.tag_name}-${tagItem.tag_color}`;

  // 如果该标识符还没有出现过，则添加到 tagListData 中
  if (!uniqueTags[tagKey]) {
    tagListData.push({
      tag_name: tagItem.tag_name,
      tag_color: tagItem.tag_color,
      tag_id: tagItem.tag_id,
    });

    // 标记该标识符为已处理
    uniqueTags[tagKey] = true;
  }
});

// 更新 tagList
tagList.value = tagListData;
      } else {
        console.error('请求失败:', response.status_msg);
      }
    })
    .catch(error => {
      console.error('请求错误:', error);
    });
});


//在后端保存修改数据接口 尚未测试
const handleSave = async() => {
  try {
    // 假设修改了 textList 和 tagList
    const updatedTextList = [...textList.value];
    // updatedTextList[0].text = "新修改的文本内容";  // 修改第一个文本项的内容

    const updatedTagList = [...tagList.value];
    // updatedTagList[0].tag_name = "新的标签名";  // 修改第一个标签的名称

    const updatedData = {
      pdf_id: pdf_id, 
      textList: updatedTextList,
      ttag: updatedTagList
    };

    console.log(updatedData);


    const response = await updateMarkContentDataService(updatedData);
    console.log(response);
    if (response.status_code === 0) {
      console.log('数据更新成功');
    } else {
      console.error('更新失败:', response.status_msg);
    }
  } catch (error) {
    console.error('更新数据失败:', error);
  }
};


// 使用 computed 来处理并拼接文本
const renderedText = computed(() => {

  return textList.value.map((content, index) => {
    // 为每一段文本生成一个唯一的 text_id
    const text_id = `text-${index}`;
    console.log(content)

    // 调用 splitText 函数处理每一段文本
    const splitContent = splitText(content.text, content.text_tag, text_id);

    // 返回该段文本的处理结果
    return `<div id="${text_id}">${splitContent.join('')}</div>`;
  }).join('');
});

//选择pdf的值
const value = ref('');

const options = [
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
];

const getTagColor = (tag_id: string): string => {
  const tag = tagList.value.find(tagItem => tagItem.tag_id === tag_id);
  return tag ? tag.tag_color : '#000000';  // 如果找不到对应的tag_id，返回默认颜色
};

const getTagName = (tag_id: string): string => {
  const tag = tagList.value.find(tagItem => tagItem.tag_id === tag_id);
  return tag ? tag.tag_name : 'Unknown';  // 如果找不到对应的tag_id，返回默认名称
};


const splitText = (text: string, text_tag: TSelectText[], text_id: string): string[] => {
  let segments: string[] = [];
  let currentIndex = 0;

  // 对实体列表按起始位置进行排序
  const sortedList = [...text_tag].sort((a, b) => a.start - b.start);

  // 遍历每个实体，处理并插入相应的 HTML
  sortedList.forEach(item => {


    // 添加实体标注之前的文本段落
    if (item.start > currentIndex) {
      segments.push(`
      <span class="text-part" id="text-part-${text_id}-${currentIndex}-${item.start}" style="line-height: 2.5;">
        ${text.substring(currentIndex, item.start)}
      </span>
      `);
    }
    // 确保传递text_id给每个实体
    const entityWithTextId = {
      ...item,
      text_id: text_id
    };

    // 添加实体标注部分
    segments.push(`
       <span class="entity-wrapper" style="display: inline-flex; flex-direction: column; margin-bottom: 0;" 
        id="entity-${text_id}-${item.start}-${item.end}" 
        onclick='handleEntityClick(event, ${JSON.stringify(entityWithTextId)})'>
        
        <span class="marked-content" style="background-color: ${getTagColor(item.tag_id)}; border-bottom: 1px solid ${getTagColor(item.tag_id)}; color: #fff; padding: 2px 4px; border-radius: 4px;">
          ${item.mark_content}
        </span>
        <span class="entity-label" style="color: ${getTagColor(item.tag_id)}; font-size: 11px; font-weight: bold; text-align: center;">
          ${getTagName(item.tag_id)}
        </span>
      </span>
    `);

    // 更新 currentIndex 为当前实体的结束位置
    currentIndex = item.end;
  });

  // 如果还有剩余的文本，添加到 segments
  if (currentIndex < text.length) {
    segments.push(`
    <span class="text-part" id="text-part-${text_id}-${currentIndex}-${text.length}" style="line-height: 2.5;">${text.substring(currentIndex)}</span>
    `);
  }

  // 拼接所有文本片段并返回
  return segments;
};

const getRandomColor = () => {
  const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', 
                 '#8A2BE2', '#FF7F50', '#20B2AA', '#9370DB', '#32CD32', '#FF4500'];
  
  // 获取已使用的颜色
  const usedColors = relationList.value.map(r => r.relation_color);
  
  // 过滤出未使用的颜色
  const availableColors = colors.filter(c => !usedColors.includes(c));
  
  // 如果有可用颜色，随机选择一个
  if (availableColors.length > 0) {
    return availableColors[Math.floor(Math.random() * availableColors.length)];
  }
  
  // 如果没有可用颜色，生成随机颜色
  let newColor;
  do {
    newColor = `#${Math.floor(Math.random()*16777215).toString(16)}`;
    // 确保生成的6位颜色代码
    while (newColor.length < 7) {
      newColor += '0';
    }
  } while (usedColors.includes(newColor));
  
  return newColor;
};



// 新增文本选择处理函数
const handleTextSelect = () => {
  const selection = window.getSelection();

  if (!selection || selection.isCollapsed) {
    tagInfo.value.visible = false;// 没有选中文本时隐藏标签框
    return;
  }

  const range = selection.getRangeAt(0);
  const rect = range.getBoundingClientRect();
  
  // 获取选中文本
  const selectedTextContent = selection.toString().trim();


  // 获取选中文本所在的段落 ID
  let text_id = '';
  let currentIndex = 0;

  // 获取选中的节点（即包含选中文本的节点）
  let selectedNode = range.startContainer;

  // 向上查找父节点，直到找到带有 id 的节点
  while (selectedNode && !(selectedNode instanceof HTMLElement)) {
    selectedNode = selectedNode.parentNode;
  }

  // 如果找到了带有 id 的节点，提取其 id 作为 text_id
  if (selectedNode && (selectedNode instanceof HTMLElement) && selectedNode.id) {
    console.log(selectedNode.id);
    text_id = selectedNode.id.split('-')[3]; // 获取段落的 text_id
    currentIndex = parseInt(selectedNode.id.split('-')[4]);
  }

  const realStart = range.startOffset + currentIndex;
  const realEnd = range.endOffset + currentIndex;

  selectedText.start = realStart;
  selectedText.end = realEnd;
  selectedText.content = selectedTextContent;
  selectedText.text_id = text_id;

  console.log(selectedText);

  // 更新标签选择框位置
  tagInfo.value = {
    visible: true,
    top: rect.bottom + window.scrollY,
    left: rect.left + (rect.width / 2) - 125 // 居中显示
  };

};




//选择标签
const handleSelectLabel = (t: TTag) => {
  const { tag_color, tag_name, tag_id } = t;
  tagInfo.value.visible = false;

  const currentText = selectedText;
  console.log(currentText.text_id);

  if (!currentText || !currentText.text_id) return;

  for (let i = 0; i < textList.value.length; i++) {
    if (i === Number(currentText.text_id)) {
      // 在找到的段落中直接添加标签
      textList.value[i].text_tag.push({
        tag_id: tag_id,
        start: currentText.start,
        end: currentText.end,
        mark_content: currentText.content,
        text_id: currentText.text_id  // 确保包含text_id
      });
      console.log(textList.value[i])
      console.log()
      break; // 找到对应段落后停止
    }
  }

  // 打印选中文本的起始位置和结束位置
  console.log(currentText.start, currentText.end);


  // 清空选中文本的信息
  selectedText.start = null;
  selectedText.end = null;
  selectedText.content = '';
  selectedText.text_id = '';  // 清空 text_id

  // 打印清空后的选中文本信息
  console.log(selectedText.start, selectedText.end);
};



const handleAllDelete = () => {
  // 清空 textList 中所有的 text_tag
  textList.value.forEach((textItem) => {
    textItem.text_tag = [];  // 清空每个文本的标注
  });

};

// const handleTagClick = (tag, event) => {
//   // 获取鼠标点击的位置
//   const mouseX = event.clientX;
//   const mouseY = event.clientY;

//   // 更新 editTag 的位置和其他信息
//   editTag.value.visible = true;
//   editTag.value.top = mouseY;
//   editTag.value.left = mouseX;
//   editTag.value.tag_id = tag.tag_id;
//   editTag.value.tag_name = tag.tag_name;
//   editTag.value.start = tag.start;
//   editTag.value.end = tag.end;
// };
// 修改 handleTagClick 函数以支持关系创建
const handleTagClick = (tag: TSelectText, event: MouseEvent) => {
   // 如果是右键点击或Ctrl+单击，则触发关系筛选
  if (event.ctrlKey || event.button === 2) {
    event.preventDefault();
    filterRelationsByEntity(tag);
    return;
  }
  event.stopPropagation();
  const element = event.currentTarget as HTMLElement;
const markedContent = element.querySelector('.marked-content') as HTMLElement;
  
  // 如果点击的是已选中的第一个实体，则取消选择
  if (relationState.firstEntity && 
      relationState.firstEntity.text_id === tag.text_id &&
      relationState.firstEntity.start === tag.start &&
      relationState.firstEntity.end === tag.end) {
    markedContent.style.boxShadow = '';
    relationState.firstEntity = null;
    return;
  }

  // 如果点击的是已选中的第二个实体，则取消选择
  if (relationState.secondEntity && 
      relationState.secondEntity.text_id === tag.text_id &&
      relationState.secondEntity.start === tag.start &&
      relationState.secondEntity.end === tag.end) {
    markedContent.style.boxShadow = '';
    relationState.secondEntity = null;
    return;
  }

  // 如果没有选中第一个实体，则设为第一个实体
  if (!relationState.firstEntity) {
    relationState.firstEntity = {
      text_id: tag.text_id,
      start: tag.start,
      end: tag.end,
      tag_id: tag.tag_id,
      element: markedContent
    };
    markedContent.style.boxShadow = '0 0 0 0.5px #1890ff';
    return;
  }

  // 如果已经选中第一个实体，则设为第二个实体
  if (!relationState.secondEntity) {
    relationState.secondEntity = {
      text_id: tag.text_id,
      start: tag.start,
      end: tag.end,
      tag_id: tag.tag_id,
      element: markedContent
    };
    markedContent.style.boxShadow = '0 0 0 0.5px #ff4d4f';

    // 检查是否有定义的关系
    createRelationIfValid();
  }
};

const createRelationIfValid = () => {
  if (!relationState.firstEntity || !relationState.secondEntity) return;

  const firstTag = tagList.value.find(t => t.tag_id === relationState.firstEntity?.tag_id);
  const secondTag = tagList.value.find(t => t.tag_id === relationState.secondEntity?.tag_id);

  if (firstTag && secondTag) {
    const foundRelation = relationList.value.find(rel => 
      (rel.entity1_name === firstTag.tag_name && rel.entity2_name === secondTag.tag_name)
    );

    if (foundRelation) {
      // 如果找到定义的关系，直接创建关系线
      relationState.relations.push({
        from: {
          text_id: relationState.firstEntity.text_id,
          start: relationState.firstEntity.start,
          end: relationState.firstEntity.end,
        },
        to: {
          text_id: relationState.secondEntity.text_id,
          start: relationState.secondEntity.start,
          end: relationState.secondEntity.end,
        },
        relation: foundRelation,
      });
      updateRelationLines();
    } else {
      // 如果没有找到定义的关系，创建临时关系线
      const tempRelationColor = getRandomColor();
      const tempRelation = {
        entity1_name: firstTag.tag_name,
        entity1_color: firstTag.tag_color,
        entity2_name: secondTag.tag_name,
        entity2_color: secondTag.tag_color,
        relation_color: tempRelationColor,
      };
      
      const tempRelationEntry = {
        from: {
          text_id: relationState.firstEntity.text_id,
          start: relationState.firstEntity.start,
          end: relationState.firstEntity.end,
        },
        to: {
          text_id: relationState.secondEntity.text_id,
          start: relationState.secondEntity.start,
          end: relationState.secondEntity.end,
        },
        relation: tempRelation,
        isTemporary: true // 标记为临时关系
      };
      
      relationState.relations.push(tempRelationEntry);
      updateRelationLines();
      
      // 高亮显示临时关系
      relationState.firstEntity.element.style.boxShadow = `0 0 0 2px ${tempRelationColor}`;
      relationState.secondEntity.element.style.boxShadow = `0 0 0 2px ${tempRelationColor}`;
    }
  }

  // 重置选择状态
  relationState.firstEntity = null;
  relationState.secondEntity = null;
};
// 更新关系线显示
const updateRelationLines = () => {
  document.querySelectorAll('.relation-line-container').forEach(el => el.remove());
  // 如果不显示关系线，直接返回
  if (!showRelations.value) return;
  relationState.relations.forEach((rel, index) => {
    // 如果启用了关系筛选，只显示匹配的关系
    if (filterState.isFiltered && filterState.activeEntity) {
      const isFromEntity = 
        rel.from.text_id === filterState.activeEntity.text_id &&
        rel.from.start === filterState.activeEntity.start &&
        rel.from.end === filterState.activeEntity.end;
      
      const isToEntity = 
        rel.to.text_id === filterState.activeEntity.text_id &&
        rel.to.start === filterState.activeEntity.start &&
        rel.to.end === filterState.activeEntity.end;
      
      if (!isFromEntity && !isToEntity) return;
    }
    if (filterState.activeRelation && 
        (rel.relation.entity1_name !== filterState.activeRelation?.entity1_name ||
         rel.relation.entity2_name !== filterState.activeRelation?.entity2_name)) {
      return;
    }
    const fromElement = document.querySelector(`#entity-${rel.from.text_id}-${rel.from.start}-${rel.from.end} .marked-content`);
    const toElement = document.querySelector(`#entity-${rel.to.text_id}-${rel.to.start}-${rel.to.end} .marked-content`);
    
    if (fromElement && toElement) {
      const container = document.createElement('div');
      container.className = 'relation-line-container';
      container.dataset.relationIndex = index.toString();
      container.style.position = 'absolute';
      container.style.top = '0';
      container.style.left = '0';
      container.style.width = '100%';
      container.style.height = '100%';
      container.style.pointerEvents = 'none';
      container.style.overflow = 'visible';
      
      const textContainer = document.getElementById('text-container');
      textContainer?.appendChild(container);
      
      const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.style.position = 'absolute';
      svg.style.width = '100%';
      svg.style.height = '100%';
      svg.style.overflow = 'visible';
      
      const fromRect = fromElement.getBoundingClientRect();
      const toRect = toElement.getBoundingClientRect();
      const containerRect = textContainer?.getBoundingClientRect() || {left: 0, top: 0};
      
      const x1 = fromRect.left - containerRect.left + fromRect.width / 2;
      const y1 = fromRect.bottom - containerRect.top;
      const x2 = toRect.left - containerRect.left + toRect.width / 2;
      const y2 = toRect.top - containerRect.top;
      
      const interactionPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
      const pathData = `M${x1},${y1} L${x2},${y2}`;
      interactionPath.setAttribute('d', pathData);
      interactionPath.setAttribute('stroke', 'transparent');
      interactionPath.setAttribute('stroke-width', '15');
      interactionPath.setAttribute('class', 'relation-interaction-path');
      interactionPath.style.cursor = 'pointer';
      interactionPath.style.pointerEvents = 'auto';
      
      interactionPath.addEventListener('click', (e) => {
        e.stopPropagation();
        if ((rel as any).isTemporary) {
          showAddRelationConfirm(index, rel.relation);
        } else {
          showDeleteConfirm(index);
        }
      });
      
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute('x1', x1.toString());
      line.setAttribute('y1', y1.toString());
      line.setAttribute('x2', x2.toString());
      line.setAttribute('y2', y2.toString());
      line.setAttribute('stroke', rel.relation.relation_color);
      
      // 根据是否是临时关系设置不同的线条样式
      if ((rel as any).isTemporary) {
        line.setAttribute('stroke-width', '2');
        line.setAttribute('stroke-dasharray', '5,3'); // 虚线样式
        line.setAttribute('class', 'relation-visual-line temporary-line');
      } else {
        line.setAttribute('stroke-width', '2');
        line.setAttribute('marker-end', 'url(#arrowhead)');
        line.setAttribute('class', 'relation-visual-line permanent-line');
      }
      
      svg.appendChild(interactionPath);
      svg.appendChild(line);
      
      // 只为正式关系添加箭头
      if (!(rel as any).isTemporary) {
        const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
        const marker = document.createElementNS("http://www.w3.org/2000/svg", "marker");
        marker.setAttribute('id', 'arrowhead');
        marker.setAttribute('markerWidth', '10');
        marker.setAttribute('markerHeight', '7');
        marker.setAttribute('refX', '9');
        marker.setAttribute('refY', '3.5');
        marker.setAttribute('orient', 'auto');
        
        const arrow = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
        arrow.setAttribute('points', '0 0, 10 3.5, 0 7');
        arrow.setAttribute('fill', rel.relation.relation_color);
        
        marker.appendChild(arrow);
        defs.appendChild(marker);
        svg.appendChild(defs);
      }
      
      container.appendChild(svg);
    }
  });
};

// 新增显示添加关系确认对话框
const showAddRelationConfirm = (index: number, relation: TRelation) => {
  ElMessageBox.confirm(
    '是否添加此关系线到关系列表？',
    '添加关系',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info',
    }
  ).then(() => {
    // 添加到关系列表
    relationList.value.push({
      entity1_name: relation.entity1_name,
      entity1_color: relation.entity1_color,
      entity2_name: relation.entity2_name,
      entity2_color: relation.entity2_color,
      relation_color: relation.relation_color
    });
    
    // 将临时关系标记为正式关系
    delete (relationState.relations[index] as any).isTemporary;
    
    // 更新显示
    updateRelationLines();
    ElMessage.success('关系已添加');
  }).catch(() => {
    // 用户取消操作
  });
};

// 显示删除确认对话框
const showDeleteConfirm = (index: number) => {
  ElMessageBox.confirm(
    '是否删除此关系线？',
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    relationState.relations.splice(index, 1);
    updateRelationLines();
    ElMessage.success('关系线已删除');
  }).catch(() => {
    // 用户取消操作
  });
};



// 在组件挂载时添加全局点击监听器，用于取消关系选择
onMounted(() => {
  document.addEventListener('click', (e) => {
    const target = e.target as HTMLElement;
    
    // 如果不是点击实体元素
    if (!target.closest('.entity-wrapper')) {
      // 取消实体筛选
      if (filterState.isFiltered) {
        filterState.activeEntity = null;
        filterState.isFiltered = false;
        updateRelationLines();
      }
      // 取消未完成的选择（只有一个实体被选中时）
      if (relationState.firstEntity && !relationState.secondEntity) {
        relationState.firstEntity.element.style.boxShadow = '';
        relationState.firstEntity = null;
      }
      
      // 隐藏标签选择框
      tagInfo.value.visible = false;
    }
  });

  
});

onMounted(() => {
  // 初始绘制
  updateRelationLines();
  
  // 监听滚动事件重新计算线位置
  const textContainer = document.getElementById('text-container');
  textContainer?.addEventListener('scroll', updateRelationLines);
  
  // 监听窗口大小变化
  window.addEventListener('resize', updateRelationLines);
});

onUnmounted(() => {
  const textContainer = document.getElementById('text-container');
  textContainer?.removeEventListener('scroll', updateRelationLines);
  window.removeEventListener('resize', updateRelationLines);
});


const handleCancel = () => {
  // 关闭编辑框，不做任何修改
  resetEditTag;
};


//重选标签
// const handleReset = () => {
//   const selection = window.getSelection();
//   if (selection && selection.rangeCount > 0) {
//     const range = selection.getRangeAt(0);
//     const start = range.startOffset;
//     const end = range.endOffset;

//     selectedText.start = start;
//     selectedText.end = end;
//     selectedText.content = selection.toString();

//     console.log(`Start: ${start}, End: ${end}`);

//     editTag.value.visible = false;
//     tagInfo.value.visible = true;

//     selection.removeAllRanges();
//   }
// };

const resetEditTag = () => {
  editTag.value = {
    visible: false,
    top: 0,
    left: 0,
    mark_id: '',
    content: '',
    tag_id: '',
    start: 0,
    end: 0,
    tag_name: '',
  }
}



const back = () => {
  // 使用 Vue Router 实现返回上一页
  router.go(-1);
};








</script>


<style scoped>

/* 关系线交互样式 */
.relation-interaction-path {
  opacity: 0;
  transition: opacity 0.2s;
}

.relation-interaction-path:hover {
  opacity: 0.2;
  stroke: #999 !important;
}

.relation-visual-line {
  transition: stroke-width 0.2s;
}

.relation-line-container:hover .relation-visual-line {
  stroke-width: 5px;
}

.el-footer .el-button {
  border-radius: 8px;
  padding: 12px 24px;
  transition: all 0.2s ease;
}

.text {
  line-height: 2;
  padding: 10px;
  font-size: 15px;

}

.el-aside{
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.information-box{
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}



.marked-content {
  position: relative;
  display: inline-block;
  border-bottom-width: 1px;
  z-index: 1; /* 确保内容在上层 */
}

.entity-label {
  position: relative;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 11px;
  font-weight: bold;
  white-space: nowrap;
  line-height: 1;
}

.tag-box {
  position: fixed;
  background: white;
  border: 1px solid #eee;
  border-radius: 4px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  z-index: 100e0;
  max-height: 300px; /* 限制最大高度 */
  overflow-y: auto; /* 添加垂直滚动条 */
}

/* 美化滚动条样式 */
.tag-box::-webkit-scrollbar {
  width: 6px;
}

.tag-box::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.tag-box::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.tag-box::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.tag-name {
  padding: 8px 12px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.2s;
}

.tag-name:hover {
  background-color: #f5f7fa;
}

.selected-text-mark {
  background-color: #ffff99;
}

.color-block-container {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-left: auto;
  margin-right: auto;
}

.color-block {
  padding: 8px 16px;
  border-radius: 25px;  /* 圆角样式 */
  color: #ffffff;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  /* 黑色勾边效果 */
  /* text-shadow: 1px 1px 2px black, -1px -1px 2px black, 1px -1px 2px black, -1px 1px 2px black; */
  text-shadow: 1px 1px 2px #888888, -1px -1px 2px #888888, 1px -1px 2px #888888, -1px 1px 2px #888888;
  /* 如果想给它一个阴影，可以使用 box-shadow */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.315);
}

.edit-tag {
  position: absolute;
  width: 120px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.edit-tag div {
  cursor: pointer;
  padding: 5px;
}

/* 保证标记文本和标签的样式 */
.marked-text,
.text-wrapper,
.text-line,
.normal-text,
.entity-container {
  display: inline;
}

.pdf-select:deep(.el-select__wrapper){
  width: 500px; /* 设置选择器的宽度 */
  border-radius: 8px;
  background: #e8fafe; /* 更深的背景颜色 */
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.05);
  height: 20px; /* 设置选择框的高度 */
  line-height: 20px; /* 保持文字垂直居中 */
  padding: 0 10px; /* 调整左右内边距 */
}

.pdf-select .el-select__prefix {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 10px; /* 根据需要调整间距 */
}

/* 调整内部输入框的样式 */
.pdf-select .el-input__inner {
  height: 20px; /* 确保内部输入框高度一致 */
  line-height: 20px;
  border-radius: 4px; /* 可选：调整圆角 */
}

.header {
  
  display: flex;
  align-items: center;
  gap: 140px;
  margin-bottom: 24px;
  padding: 16px 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.title {
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 8px;
}
.icon {
  width: 32px; /* 图标的宽度 */
  height: 32px; /* 图标的高度 */
  fill: currentColor; /* 图标颜色 */
}

.search-container {
  flex: 1;
  max-width: 500px;
  margin-left: auto;
  position: relative;
}

.relationship-block-container {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-left: auto;
  margin-right: auto;
}

.relationship-block {
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.2s;
  border-radius: 8px;
}

.relationship-block:hover {
  background-color: #f5f5f5;
  transform: scale(1.05);
}

.relationship-block.filtered {
  background-color: #e6f7ff;
  box-shadow: 0 0 0 2px #1890ff;
}

/* 添加提示文字 */
.relationship-filter-hint {
  font-size: 12px;
  color: #888;
  margin-top: 5px;
  text-align: center;
}

.entity-block {
  padding: 8px 16px;
  border-radius: 25px;  /* 圆角样式 */
  color: #ffffff;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  /* 黑色勾边效果 */
  text-shadow: 1px 1px 2px #888888, -1px -1px 2px #888888, 1px -1px 2px #888888, -1px 1px 2px #888888;
  /* 如果想给它一个阴影，可以使用 box-shadow */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.315);
}

.relation-line {
  font-weight: bold;
  font-size: 14px;
  margin: 0 5px; /* 调整关系线的间距 */
}
.separator {
  border: 0;
  height: 1px;
  background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
  margin: 20px 0; /* 调整上下间距 */
}

.entity-wrapper {
  cursor: pointer;
  transition: box-shadow 0.2s;
  position: relative;
  display: inline-block;
  margin: 0 2px;
  line-height: 1.2;
}

.entity-wrapper:hover .marked-content,
.entity-wrapper.selected .marked-content {
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.3);
}

.relation-line-element {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 100;
  overflow: visible;
}

.relation-line-element line {
  stroke-width: 2px;
  stroke-dasharray: 0;
}

.relation-line-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: visible;
}

/* 关系线 */
.relation-line-container svg {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: visible;
}

.relation-line-container line {
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* 删除按钮 */
.relation-delete-btn {
  width: 20px;
  height: 20px;
  background: #ff4d4f;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  pointer-events: auto;
  transition: all 0.2s;
}

.relation-delete-btn:hover {
  transform: scale(1.2);
  background: #ff7875;
}

.temporary-line {
  stroke-dasharray: 5,3; /* 虚线样式 */
  animation: dash-animation 1s linear infinite;
}

@keyframes dash-animation {
  to {
    stroke-dashoffset: 8; /* 虚线动画效果 */
  }
}

.permanent-line {
  stroke-dasharray: none; /* 实线 */
}

/* 临时关系的悬停效果 */
.temporary-line:hover {
  stroke-width: 3px !important;
  stroke-dasharray: none !important;
  animation: none !important;
}

.entity-filter-hint {
  font-size: 12px;
  color: #888;
  margin-top: 5px;
  text-align: center;
}

.entity-wrapper.filtered {
  box-shadow: 0 0 0 2px #ff4d4f;
}
/* 关系线切换按钮样式 */
.relation-toggle-btn {
  position: absolute;
  right: 20px;
  top: 20px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.relation-toggle-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>