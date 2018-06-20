
# coding: utf-8

# In[1]:


get_ipython().run_cell_magic('html', '', '<script>\n  function code_toggle() {\n    if (code_shown){\n      $(\'div.input\').hide(\'500\');\n      $(\'#toggleButton\').val(\'Show Code\')\n    } else {\n      $(\'div.input\').show(\'500\');\n      $(\'#toggleButton\').val(\'Hide Code\')\n    }\n    code_shown = !code_shown\n  }\n\n  $( document ).ready(function(){\n    code_shown=false;\n    $(\'div.input\').hide()\n  });\n</script>\n<form action="javascript:code_toggle()"><input type="submit" id="toggleButton" value="Show Code"></form>')


# In[4]:


# database connection
import os
import psycopg2
from sqlalchemy.engine.url import URL

# connection to the database
# connection string for use in pandas:
con = str(URL(drivername='postgresql', 
              username=os.environ['DB_QIR_USERNAME'], 
              password=os.environ['DB_QIR_PASSWORD'], 
              host='www.quantleap.nl', 
              database='qir'))

# cursor for use with psycopg2
conn = psycopg2.connect(con)
cur = conn.cursor()

# todo: use NamedTupleCursor


# In[10]:


import ipywidgets as widgets
from ipywidgets import Layout
from IPython.display import display

class ReportTextSearcher(object):
    def __init__(self):
        self.sections = ['--- Gehele verslag',
                         '0.0 Introduction', 
                         '1.7 Oorzaak faillissement', 
                         '7.6 Paulianeus handelen', 
                         '8.1 Boedelvorderingen']
        
        self.results = []
        
        # widgets, more clear to define that to access by container tuple
        self.w_search_terms = widgets.Text(description='Zoektermen', value='rabobank abn amro')
        self.w_section = widgets.Dropdown(options=self.sections, description='hoofdstuk')
        self.w_button = widgets.Button(description='Zoek', layout={'margin': '5px 0px 0px 90px', 'width': '212px'})
        self.w_limit = widgets.IntSlider(value=10, min=10, max=200, step=10, description='limit')
        self.w_result_no = widgets.IntSlider(value='1', min='1', description='view result', disabled=True)
        self.w_result = widgets.Textarea(layout={'width': '90%', 'height': '100px', 'margin': '5px 0'}) 
        self.w_out = widgets.Output()
        
        # container of widgets
        self.container = widgets.VBox([
            self.w_search_terms,
            self.w_section,
            self.w_limit,
            self.w_button,
            self.w_out,
            self.w_result,
            self.w_result_no
        ])
        
        # register callbacks
        self.w_button.on_click(self._search)
        self.w_result_no.observe(self._view_result, 'value')
        
        #import pdb; pdb.set_trace()
        
    def render(self):
        display(self.container)

    def _render_results(self):
        # process results
        self.w_out.append_stdout('{:d} resultaten gevonden'.format(len(self.results)))
        self.w_result_no.max = len(self.results)
        
        if len(self.results) > 0:
            # show first result
            self.w_result_no.disabled = False
            self.w_result_no.value = 1
            self.w_result.value = self.results[0][1]
        
    # call backs
    def _view_result(self, change):
        result = self.results[self.w_result_no.value -1]
        self.w_result.value = result[1]
        
    def _search(self, button):
        # reset
        self.w_result.value = ''
        self.w_out.clear_output()
        self.w_result_no.disabled = True
        
        # search
        field = 'content'
        query_terms = 'rabobank abn amro'
        
        sql = """WITH eligible_reports AS (
                     SELECT identification, {field} AS content
                     FROM reports rep join insolvents ins on rep.insolvent_id = ins.id
                     WHERE publication_date BETWEEN '2014-01-01' AND '2017-12-31'
                         AND ins.is_removed = FALSE)
                 SELECT identification, {field} as content
                 FROM eligible_reports
                 WHERE to_tsvector('dutch', {field}) @@ plainto_tsquery('dutch', '{query_terms}') LIMIT {limit};""".format(field=field, query_terms=query_terms, limit=self.w_limit.value)
        
        #print(sql)
        cur.execute(sql)
        self.results = cur.fetchall()
        
        self._render_results()


# In[11]:


search = ReportTextSearcher()
search.render()


# In[ ]:


cur.close()


# # Postgres and full text search support
# 
# Postgres supports normalization and lemmatization for the Dutch language.
# 

# In[ ]:




