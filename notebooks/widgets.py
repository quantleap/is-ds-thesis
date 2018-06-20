
# coding: utf-8

# In[106]:


import ipywidgets as widgets
from ipywidgets import Layout, interact, interactive, fixed, interact_manual


# In[2]:


def search_section(section, search_string, limit=10):
    return "this is my result for section " + section


# # Interact

# In[3]:


interact(search_section, section='7.6', search_string='paulianeus', limit=fixed(10));


# # Interactive

# In[4]:


from IPython.display import display
def f(a, b):
    display(a + b)
    return a+b


# In[5]:


f(1, 2)


# In[6]:


widget = interactive(f, a=10, b=20)
type(widget)


# In[7]:


widget.children


# In[8]:


display(widget)


# In[9]:


print(widget.kwargs)
print(widget.result)


# # Widgets

# In[10]:


widgets.Dropdown(
    options={'One': 1, 'Two': 2, 'Three': 3},
    value=2,
    description='Number:',
)


# In[11]:


widgets.Text(
    value='Hello World',
    placeholder='Type something',
    description='String:',
    disabled=False
)


# In[114]:


widgets.Textarea()


# In[12]:


# The date picker widget works in Chrome and IE Edge, but does not currently work in Firefox or Safari 
widgets.DatePicker(
    description='Pick a Date',
    disabled=False
)


# ## Form Elements

# In[13]:


# search keyword
w_search = widgets.Text(placeholder='b.v. fraude', description='Zoektermen')
display(w_search)


# In[14]:


# limit results
w_limit = widgets.IntSlider(value=10, min=10, max=200, step=10, description='limit')
display(w_limit)


# In[15]:


# section dropdown
sections = ['0.0 Introduction', '1.7 Oorzaak faillissement', '7.6 Paulianeus handelen', '8.1 Boedelvorderingen']
w_section = widgets.Dropdown(options=sections, description='hoofdstuk')
display(w_section)


# In[103]:


# alternative section multiselect
w = widgets.SelectMultiple(options=sections, description='hoofdstuk')
display(w)


# In[17]:


# and search button
w_button = widgets.Button(description='Zoek')
display(w_button)


# In[18]:


# publication period 
w_start_date = widgets.DatePicker(description='Start')
w_end_date = widgets.DatePicker(description='End')
display(widgets.HBox([w_start_date, w_end_date]))


# In[86]:


# publication period
import datetime
from dateutil.relativedelta import relativedelta

start_date = datetime.date(2014, 1, 1)
dates = [start_date + relativedelta(months=i) for i in range(49)]
options = [i.strftime('%Y%m') for i in dates]

w_period = widgets.SelectionRangeSlider(options=options, description='periode')
display(w_period)


# In[88]:


# output
w_out = widgets.Output()


# In[125]:


# alternative a text area
w_out = widgets.Textarea(layout={'width': '90%', 'height': '100%'})


# In[60]:


# show result number ..
w_result_no = widgets.IntSlider(min=1, max=20, description='result number')
display(w_result_no)


# ## Layout

# In[116]:


# box (flexbox)
widgets.Box([w_search, w_section, w_button])


# In[117]:


# horizontal box
widgets.HBox([w_search, w_section, w_button])


# In[126]:


# vertical box
widgets.VBox([w_search, w_section, w_button, w_out])


# In[127]:


# write std output to out and clear
import time
with w_out:
    for i in range(10):
        print(i, "Hello World")
time.sleep(5)
w_out.clear_output()


# ## Events

# In[100]:


def on_button_clicked(b):
    print("Zoeken...")

w_button.on_click(on_button_clicked)
# try in vertical box above


# ## Resulting form with styling

# In[101]:


w_button.layout = Layout(margin='5px 0px 0px 90px', width='212px')
w_out.layout=(Layout(border='1px solid black', margin='10px'))


# In[128]:


search_box = widgets.VBox([w_search, w_section, w_limit, w_button, w_out, w_result_no])

w_out.value = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui.'
display(search_box)


# In[ ]:




