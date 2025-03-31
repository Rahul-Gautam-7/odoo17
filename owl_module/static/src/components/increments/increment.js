/** @odoo-module */

import {registry} from "@web/core/registry";
import {Component,useState} from "@odoo/owl";

export class Increment extends Component{

    setup(){
        this.state=useState({value:0});
    }

    increment(){
        this.state.value++;
    }
}

Increment.template='owl_module.increment';

registry.category('actions').add('owl.increment_js',Increment);