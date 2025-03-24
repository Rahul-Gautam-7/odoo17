from odoo import http

class ControllFun(http.Controller):

    # @http.route('/academy/',auth='public')
    # def index(self,**kw):
    #     return http.request.render('testing_module.tester',{
    #         'students':
    #         ['Rahul','Yuvraj','Vidhey','Vatsal'],
    #     })

    @http.route('/modelss/datas/',auth='public',website=True)
    def model_display_data(self,**kw):
        datas=http.request.env['test.module'].search([])
        return http.request.render('testing_module.tempss',{
            "datas":datas
        })

    # @http.route('/url/views/<name>',auth='public',website=True)
    # def display_url_values(self,name):
    #     return "<h1>{}</h1>".format(name)

    # @http.route('/url/views/<int:id>',auth='public',website=True)
    # def display_url_values(self,id):
    #     return "<h1>{}</h1>".format(id)

    @http.route("/modelss/<model('test.module'):data>/",auth='public',website=True)
    def display_details(self,data):
        return http.request.render('testing_module.temps_detail',{'data':data})