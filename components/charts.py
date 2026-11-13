import plotly.express as px
import plotly.graph_objects as go
from config import COLORS

LAYOUT=dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#CBD5E1",family="DM Sans"),margin=dict(l=12,r=12,t=48,b=12),legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.12),hoverlabel=dict(bgcolor="#1B2336",font_color="#F8FAFC"))

def finish(fig, height=360):
    fig.update_layout(**LAYOUT,height=height)
    fig.update_xaxes(gridcolor="#263349",linecolor="#334155",zerolinecolor="#334155",title_font_color="#CBD5E1",tickfont_color="#CBD5E1")
    fig.update_yaxes(gridcolor="#263349",linecolor="#334155",zerolinecolor="#334155",title_font_color="#CBD5E1",tickfont_color="#CBD5E1")
    return fig

def bar(data,x,y,title,color=None,horizontal=False):
    fig=px.bar(data,x=y if horizontal else x,y=x if horizontal else y,color=color or x,color_discrete_sequence=COLORS, title=title,orientation="h" if horizontal else "v",text_auto=".2s")
    fig.update_traces(marker_line_width=0)
    return finish(fig)

def line(data,x,y,title,color=None):
    fig=px.line(data,x=x,y=y,color=color,markers=True,color_discrete_sequence=COLORS,title=title)
    fig.update_traces(line_width=3,marker_size=6)
    return finish(fig)


