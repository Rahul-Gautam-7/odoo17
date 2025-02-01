from odoo import api,fields,models
import logging

_logger = logging.getLogger(__name__)

class Reporte(models.AbstractModel):
    _name="report.rg_library.enroll_stud_xlsx"
    _inherit='report.report_xlsx.abstract'
    
    
    
    
    
    def generate_xlsx_report(self,workbook,data,objects):
        sheet= workbook.add_worksheet('Custom Report')
        bold=workbook.add_format({'bold':True,'align':'center','valign':'vcenter'})
        heading_format=workbook.add_format({'bold':True,'align':'center','valign':'vcenter','font_size':14})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'align': 'center', 'valign': 'vcenter'})        
        sheet.set_column('A:Z',15)
        
        
        sheet.write(0,0,'Date',bold)
        sheet.write(1,0,'Customer Name',bold)
        sheet.write(2,0,'Payment Terms',bold)
        _logger.info(objects.curr_date)
        sheet.write(0,1,objects.curr_date,date_format)
        sheet.write(1,1,objects.student_id.name)
        sheet.write(2,1,objects.ref)
        
        
        
        sheet.merge_range('A4:G5','Order Line',heading_format)
        
        
        sheet.write(5,0,'No',bold)
        sheet.write(5,1,'Product Code',bold)
        sheet.write(5,2,'Product Name',bold)
        sheet.write(5,3,'Quantity',bold)
        sheet.write(5,4,'Unit Price',bold)
        sheet.write(5,5,'Total Price',bold)
        
        row = 6
        i=1
        total=0
        for record in objects:
            for line in record.book_line_ids:
                sheet.write(row,0,i)
                sheet.write(row,1,line.product_id.default_code)
                sheet.write(row,2,line.product_id.name)
                sheet.write(row,3,line.qty)
                sheet.write(row,4,line.price)
                sheet.write(row,5,line.price_subtotal)
                total+=line.price_subtotal
                row+=1
                i+=1 
                
        sheet.write(row,5,total)
    
    
    @api.model
    def _get_report_values(self,docids,data=None):
        enroll_stud = self.env['enroll.stud'].browse(docids)
        report_name = f"Enrollment_Report_{enroll_stud.ref}_{enroll_stud.curr_date}.xlsx"
        return {
            'doc_ids': docids,
            'doc_model': 'enroll.stud',
            'report_name':report_name, 
            'data': data,
        }
    