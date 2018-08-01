
# coding: utf-8

# In[1]:


get_ipython().run_cell_magic('html', '', '<script>\n  function code_toggle() {\n    if (code_shown){\n      $(\'div.input\').hide(\'500\');\n      $(\'#toggleButton\').val(\'Show Code\')\n    } else {\n      $(\'div.input\').show(\'500\');\n      $(\'#toggleButton\').val(\'Hide Code\')\n    }\n    code_shown = !code_shown\n  }\n\n  $( document ).ready(function(){\n    code_shown=false;\n    $(\'div.input\').hide()\n  });\n</script>\n<form action="javascript:code_toggle()"><input type="submit" id="toggleButton" value="Show Code"></form>')


# In[2]:


# database connection
import os
import psycopg2
from sqlalchemy.engine.url import URL

# connection to the database
# connection string for use in pandas:
con = str(URL(drivername='postgresql', 
              username=os.environ['DB_QIR_USERNAME'], 
              password=os.environ['DB_QIR_PASSWORD'], 
              # host='www.quantleap.nl', 
              host='localhost', 
              database='qir'))

# cursor for use with psycopg2
conn = psycopg2.connect(con)
cur = conn.cursor()

# todo: use NamedTupleCursor


# In[2]:


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
        self.w_query_terms = widgets.Text(description='zoektermen')
        self.w_section = widgets.Dropdown(options=self.sections, description='sectie')
        self.w_button = widgets.Button(description='Zoek', layout={'margin': '5px 0px 0px 90px', 'width': '212px'})
        self.w_limit = widgets.IntSlider(value=10, min=10, max=200, step=10, description='limiet')
        self.w_result_no = widgets.IntSlider(value='1', min='1', description='bekijk #', disabled=True)
        #self.w_result = widgets.HTML()
        self.w_out = widgets.Output()
        
        # container of widgets
        self.container = widgets.VBox([
            widgets.HTML('<h1>Rapporten doorzoeken</h1>'),
            self.w_query_terms,
            self.w_section,
            self.w_limit,
            self.w_button,
            self.w_result_no,
            self.w_out 
            #self.w_result
        ])
        
        # register callbacks
        self.w_button.on_click(self._search)
        self.w_result_no.observe(self._change_result, 'value')
        
        #import pdb; pdb.set_trace()
        
    def render(self):
        display(self.container)

    def _render_results(self):
        # process results
        self.w_result_no.max = len(self.results)
        
        if len(self.results) > 0:
            # show first result
            self.w_result_no.disabled = False
            self.w_result_no.value = 1
            self.w_out.append_stdout(self.results[0][1])
        
    # call backs
    def _change_result(self, change):
        #self.w_out.clear_output(wait=True)
        result = self.results[self.w_result_no.value - 1][1]
        self.w_out.append_stdout(result)

    def _get_result_tag(self, content):
        return "<p style='border: 1px solid grey; padding: 10px; background-color: Azure;'>{}</p>".format(content)
    
    def _search(self, button):
        # reset
        self.w_result_no.disabled = True
        
        # search
        field = 'content'
        
        sql = """WITH eligible_reports AS (
                     SELECT identification, {field} AS content
                     FROM reports rep join insolvents ins on rep.insolvent_id = ins.id
                     WHERE publication_date BETWEEN '2014-01-01' AND '2017-12-31'
                         AND ins.is_removed = FALSE)
                 SELECT identification, {field} as content
                 FROM eligible_reports
                 WHERE to_tsvector('dutch', {field}) @@ plainto_tsquery('dutch', '{query_terms}') LIMIT {limit};""".format(field=field, query_terms=self.w_query_terms.value, limit=self.w_limit.value)
        
        cur.execute(sql)
        self.results = cur.fetchall()
        self._render_results()


# In[3]:


search = ReportTextSearcher()
search.render()


# In[ ]:


# vergelijk ES en postgres functionaliteit
# query parsing, meerdere secties tegelijk - patent search total recall
# permanent identifier naar reproduceerbare content.! voor discussie. wetenschappelijke
# mysociety
# persona - use cases  evaluatie taak. verschil met huidige situatie.


# skeleton verslag met bullet points van alles wat er doen is.
# ..

