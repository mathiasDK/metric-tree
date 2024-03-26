import plotly.graph_objects as go
import plotly.express as px

import polars as pl

class Plotter:
    def __init__(self) -> None:
        self.primary_colors = {
            "bordeaux": "#462023",
            "green": "#234620",
            "blue": "#005288",
            "orange": "#DD663C"
        }
        self.secondary_colors = {
            "dark_grey": "#30373b",
            "light_grey": "#979b9d",
            "bordeaux": "#a28f91",
            "green": "#91a28f",
            "blue": "#7fa8c3",
            "orange": "#eeb29d"
        }
        self.divergent_colors = {
            "good": "#462023",
            "mid": "#979b9d",
            "bad": "#005288",
        }
        self.colorway=["#005288", "#DD663C", "#492a42", "#234620", "#F5CC5B", "#30373b", "#E5C0D1",]
        self._create_layout_template()

    def _create_layout_template(self):
        fig = px.line(
            x=[1,2], y=[1,2],
            template="simple_white"
        )
        fig.update_layout(
            plot_bgcolor="#f8f5e7",
            paper_bgcolor="#f8f5e7",
            colorway=["#005288", "#DD663C", "#492a42", "#234620", "#F5CC5B", "#30373b", "#E5C0D1",],
            # margin=dict(r=10, l=10, b=10, t=50),
            yaxis=dict(rangemode="tozero", showgrid=False, showline=True, linewidth=1, linecolor="black"),
            xaxis=dict(showgrid=False, showline=True, linewidth=1, linecolor="black")
        )
        self.layout_template = dict(
            layout=fig.layout
        )
    
    def _set_end_label(self, fig, x, y, text, color):
        """
        This function should be used to create labels at the right side of the graph

        Args:
            x (float): The most right variable on the x axis
            y (float): The height of the label
            text (str): The label text
            color (str): The hex color of the text (same as line)
        """
        fig.add_trace(
            go.Scatter(
                x=[x], y=[y], text=[text],
                mode="markers+text",
                marker=dict(color=color, size=15),
                textfont=dict(color=color, size=15),
                textposition="middle right",
                name=f"{x},{y}",
                showlegend=False
            )
        )
        return fig

    def line_plot(self, df, x, y, comparison_type:str=None, color:str=None) -> go.Figure:
        color_dict = {}
        if comparison_type is not None:
            groups = df[color].unique()
            color_dict = {}
            if comparison_type=="experiment":
                for i, group in enumerate(groups):
                    if group.lower() == "control":
                        color_dict[group] = self.secondary_colors["light_grey"]
                    else:
                        color_dict[group] = self.colorway[i]
        elif color is not None:
            for i, c in enumerate(df[color].unique()):
                color_dict[c] = self.colorway[i]
        # Plotting
        fig = px.line(
            df,
            x=x, y=y,
            color=color,
            color_discrete_map=color_dict,
            template = self.layout_template
        )

        # Adding end labels
        for d in fig.data:
            x = d["x"][-1]
            y = d["y"][-1]
            color = d["line"]["color"]
            fig = self._set_end_label(fig, x, y, str(y), color)

        return fig
    
if __name__ == "__main__":

    df = pl.DataFrame(data={
        "x": ["a", "b", "c", "d", "a", "b", "c", "d"], 
        "y": [4,3,2,3,3.9,3.1,4,4], 
        "color": ["control","control","control","control","variant","variant","variant","variant",]})
    p = Plotter()
    fig = p.line_plot(df, x="x", y="y", comparison_type="experiment", color="color")
    fig.show()