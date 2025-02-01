from odoo import api,fields,models


class Reporte(models.AbstractModel):
    _name="report.cust.reporte"
    _inherit='report.report_xlsx.abstract'
    
    def myxlsx(self,workbook,data,objects):
        sheet= workbook.add_worksheet('Custom Report')
        bold=workbook.add_format({'bold':True,'align':'center','valign':'vcenter'})
        heading_format=workbook.add_format({'bold':True,'align':'center','valign':'vcenter','font_size':14})        
        
        sheet.merge_range('A1:C1','Order Line',heading_format)
        
        sheet.write(0,0,'No',bold)
        sheet.write(0,1,'Product Code',bold)
        sheet.write(0,2,'Product Name',bold)
        sheet.write(0,3,'Quantity',bold)
        sheet.write(0,4,'Unit Price',bold)
        sheet.write(0,5,'Taxes',bold)
        sheet.write(0,6,'Total Price',bold)
        
        row = 2
        for record in objects:
            for line in record.order_line:
                sheet.write(row,0,record)
                sheet.write(row,1,line.product_id.default_code)
                sheet.write(row,2,line.product_id.name)
                sheet.write(row,3,line.product_uom_qty)
                sheet.write(row,4,line.price_unit)
                sheet.write(row,5,', '.join([tax.name for tax in line.tax_id]))
                sheet.write(row,6,line.price_subtotal)
                row+=1 