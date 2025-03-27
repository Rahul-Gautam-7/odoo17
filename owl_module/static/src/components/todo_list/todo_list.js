/** @odoo-module **/
import {registry} from '@web/core/registry'
const {Component,useState,onWillStart,useRef} = owl;
import {useService} from "@web/core/utils/hooks"


export class OwlTodoList extends Component {
 
    setup()
    {
        this.state = useState({
            task:{name:"",color:"#ff0000",completed:false},
            taskList:[],
            isEdit:false,
            activeId:false,
        })
        this.orm = useService("orm")
        this.model = "owl.todo.list"
        this.searchInput = useRef("search-input")

        onWillStart(async ()=>{
            await this.getAllStart()  
        })
    }
    async getAllStart(){
        this.state.taskList = await this.orm.searchRead(this.model,[],["name","color","completed"])
    }

    addTask(){
        this.resetForm()
        this.state.activeId=false
        this.state.isEdit=false
    }

    async editTask(task){
        
            this.state.activeId=task.id
            this.state.isEdit = true
            this.state.task={name:task.name,color:task.color,completed:task.completed}
            await this.getAllStart()
    }

    async saveTask(){
        console.log(this.state.task)
        if(!this.state.isEdit){
            await this.orm.create(this.model,[this.state.task])
        }
        else {
            await this.orm.write(this.model,[this.state.activeId],this.state.task)
        }
        await this.getAllStart()
    }

    async deleteTask(task){
        await this.orm.unlink(this.model,[task.id])
        await this.getAllStart()
    }

    async toggleTask(e,task){
        await this.orm.write(this.model,[task.id],{completed:e.target.checked})
        await this.getAllStart()
    }

    async updateColor(e,task){
        await this.orm.write(this.model,[task.id],{color:e.target.value})
        await this.getAllStart()
    }

    async searchTasks(){
        const text = this.searchInput.el.value
        console.log(text)
        this.state.taskList = await this.orm.searchRead(this.model,[['name','ilike',text]],["name","color","completed"])
    }

    resetForm(){
        this.state.task = {name:"",color:"#ff0000",completed:false}
    }
}


OwlTodoList.template='owl.TodoList'
registry.category('actions').add('owl.action_todo_list_js',OwlTodoList);