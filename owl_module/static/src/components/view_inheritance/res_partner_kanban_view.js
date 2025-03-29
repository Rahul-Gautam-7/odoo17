/** @odoo-module */

import {registry} from "@web/core/registry"
import {kanbanView} from "@web/views/kanban/kanban_view"
import {KanbanController} from "@web/views/kanban/kanban_controller"
import {useService} from "@web/core/utils/hooks"


const {onWillStart} =owl;

class ResPartnerKanbanController extends KanbanController{
    setup()
    {   
        super.setup()
        console.log("This is a res partner controller")
        console.log("searchModel:", this.env.searchModel);
        this.action = useService("action")
        this.orm = useService("orm")

        onWillStart(async ()=>{
            this.customerLocations = await this.orm.readGroup("res.partner",[],['state_id'],['state_id'])
            console.log(this.customerLocations)
        })

    }

    openSalesView(){
        console.log("OPen sales view is triggered")
        this.action.doAction({
            type:"ir.actions.act_window",
            name:"Customer Sales",
            res_model:"sale.order",
            views:[[false, "list"],[false, "form"]]
        })
    }


    selectLocations(state){
        const id = state[0]
        const name = state[1]
        
        console.log("searchModel:", this.env.searchModel); // Debug: Check if searchModel exists
        console.log("searchModel methods:", Object.keys(this.env.searchModel || {})); // List available methods

        if (this.env && this.env.searchModel) {
            console.log("This is a res partner controller");
            console.log("searchModel:", this.env.searchModel);
        
            // Set the domain
            this.env.searchModel._domain = [["state_id", "=", id]];
        
            // Try to reload the search model
            if (typeof this.env.searchModel.reload === "function") {
                console.log("Reloading searchModel...");
                this.env.searchModel.reload();
            } else if (typeof this.env.searchModel.load === "function") {
                console.log("Loading searchModel...");
                this.env.searchModel.load();
            } else {
                console.warn("No reload/load function on searchModel, falling back to doAction");
                this.action.doAction({
                    type: "ir.actions.act_window",
                    res_model: "res.partner",
                    views: [[false, "kanban"]],
                    domain: [["state_id", "=", id]],
                    context: { search_default_name: name },
                    target: "current",
                });
            }
        } else {
            console.error("searchModel unavailable, falling back to doAction");
            this.action.doAction({
                type: "ir.actions.act_window",
                res_model: "res.partner",
                views: [[false, "kanban"]],
                domain: [["state_id", "=", id]],
                context: { search_default_name: name },
                target: "current",
            });
        }
    }

}

ResPartnerKanbanController.template = "owl.ResPartnerKanbanView"

export const resPartnerKanbanView = {
    ...kanbanView,
    Controller : ResPartnerKanbanController,
    buttonTemplate : "owl.ResPartnerKanbanView.Buttons",
}

registry.category("views").add("res_partner_kanban_view",resPartnerKanbanView)