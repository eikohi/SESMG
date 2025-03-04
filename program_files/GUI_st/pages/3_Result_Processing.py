"""
    jtock - jan.tockloth@fh-muenster.de
    GregorBecker - gregor.becker@fh-muenster.de
    janik257
"""
import glob
import os
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
import plotly.express as px
from PIL import Image

from program_files.GUI_st.GUI_st_global_functions import \
    import_GUI_input_values_json, st_settings_global, read_markdown_document


def result_processing_sidebar():
    """
        Function to create the sidebar.
    """

    # Import GUI help comments from the comment json and safe as an dict
    GUI_helper = import_GUI_input_values_json(
        os.path.dirname(os.path.dirname(__file__))
        + "/GUI_st_help_comments.json")

    # create sidebar
    with st.sidebar:
        st.header("Result Overview")

        # read sub folders in the result folder directory
        existing_result_foldernames_list = [
            os.path.basename(x) for x in glob.glob(f'{"results/*"}')]
        existing_result_foldernames_list.sort()
        # create select box with the folder names which are in the results folder
        existing_result_folder = st.selectbox(
            label="Choose the result folder",
            options=existing_result_foldernames_list,
            help=GUI_helper["res_dd_result_folder"])

        # check box if user wants to reload existing results
        run_existing_results = st.button(label="Load Existing Results",
                                         help=GUI_helper["res_b_load_results"])

        if run_existing_results:
            # set session state with full folder path to the result folder
            st.session_state["state_result_path"] = \
                os.path.join(os.path.dirname(os.path.dirname(
                                os.path.dirname(os.path.dirname(
                                    os.path.abspath(__file__))))),
                             "results",
                             existing_result_folder)

        if st.session_state["state_result_path"] != "not set" and \
                os.path.join(st.session_state["state_result_path"],
                             "components.csv") \
                not in glob.glob(st.session_state["state_result_path"] + "/*"):
            # header
            st.header("Pareto Results")

            # read out sub folders of pareto list
            existing_result_foldernames_list = next(
                os.walk(st.session_state["state_result_path"]))[1]
            # split folder names and safe pareto point positions in a list
            pareto_points_list = [directory.split(
                "_")[-2] for directory in existing_result_foldernames_list]

            # create dict with pareto point positions and folder names
            pareto_folder_dict = dict(
                zip(pareto_points_list, existing_result_foldernames_list))
            # sort pareto point list
            pareto_points_list.sort()
            # create select box to choose the pareto point you want to see
            # show results for
            pareto_point_chosen = st.selectbox(
                label="Choose the pareto point",
                options=pareto_points_list,
                help=GUI_helper["res_dd_pareto_point"])

            # create session_state to initialize the pareto result overviews
            st.session_state["state_pareto_point_chosen"] = pareto_point_chosen
            st.session_state["state_pareto_result_path"] = \
                os.path.join(st.session_state["state_result_path"],
                             pareto_folder_dict[pareto_point_chosen])
            # st.session_state["state_pareto_result_path"] = \
            #     st.session_state["state_result_path"] + \
            #     "/" + pareto_folder_dict[pareto_point_chosen]


def short_result_summary_time(result_path_summary):
    """
        Function displaying the results time series informations.

        :param result_path_summary: path to a result summary.csv file
        :type result_path_summary: str
    """
    st.subheader("Result Overview")
    # Import summary.csv and create dataframe
    df_summary = pd.read_csv(result_path_summary)
    # Display and import time series values
    # adding two blank rows
    time1, time2, time3, time4 = st.columns(4)
    time1.metric(label="Start Date", value=str(df_summary.iloc[0, 0]))
    time2.metric(label="End Date", value=str(df_summary.iloc[0, 1]))
    # TODO: Problem Darstellung Temporal Resolution
    # time3.metric(label="Temporal Resolution", \
    #    value=str(df_summary['Resolution']))


def short_result_summary_system(result_path_summary):
    """
        Function displaying the short result summary overview of the energy \
            system.

        :param result_path_summary: path to a result summary.csv file
        :type result_path_summary: str
    """
    # Import summary.csv and create dataframe
    df_summary = pd.read_csv(result_path_summary)
    # Create list with headers
    summary_headers = list(df_summary)
    # format thousands separator
    # TODO: Tausendertrennung
    # df_summary = df_summary.iloc[1,:].style.format(thousands=" ",precision=0)
    # TODO: add delta functions based on the latest results
    # Display and import simulated cost values from summary dataframe
    cost1, cost2, cost3, cost4 = st.columns(4)
    cost1.metric(label=summary_headers[3], value=round(
        df_summary[summary_headers[3]], 1))
    cost2.metric(label=summary_headers[4], value=round(
        df_summary[summary_headers[4]], 1))
    cost3.metric(label=summary_headers[5], value=round(
        df_summary[summary_headers[5]], 1))
    cost4.metric(label=summary_headers[6], value=round(
        df_summary[summary_headers[6]], 1))

    # Display and import simulated energy values from summary dataframe
    # adding two blank rows
    ener1, ener2, ener3, ener4 = st.columns(4)
    ener1.metric(label=summary_headers[7], value=round(
        df_summary[summary_headers[7]], 1))
    ener2.metric(label=summary_headers[8], value=round(
        df_summary[summary_headers[8]], 1))


def short_result_simplifications(result_GUI_settings_dict):
    """
        Function to display model simplification settings in addition
            to the timeseries information.
        :param result_path_components: dict including the last runs GUI
            settings
        :type result_path_components: dict
    """
    alg1, alg2 = st.columns(2)
    alg1.metric(label="Simplification Algorithm",
                value=result_GUI_settings_dict["input_timeseries_algorithm"])
    # create 5 columns. one for each simplification input field
    simp1, simp2, simp3, simp4 = st.columns(4)
    simp1.metric(
        label="Simplification Index",
        value=result_GUI_settings_dict["input_timeseries_cluster_index"])
    simp2.metric(
        label="Cluster Criterion",
        value=result_GUI_settings_dict["input_timeseries_criterion"])
    simp3.metric(
        label="Simplification Period",
        value=result_GUI_settings_dict["input_timeseries_period"])
    simp4.metric(
        label="Cluster Season",
        value=result_GUI_settings_dict["input_timeseries_season"])


def short_result_premodelling(result_GUI_settings_dict):
    """
        Function to display premodel settings in addition to
            the timeseries information.

        :param result_path_components: dict including the last
            runs GUI settings
        :type result_path_components: dict
    """
    # check if investment boundaries were active to show tightening factor
    # create columns for pre-modelling information
    # adding one optional for tightening factor and one blank
    pre1, pre2, pre3, pre4 = st.columns(4)
    pre1.metric(
        label="Premodelling Active",
        value=result_GUI_settings_dict["input_activate_premodeling"])
    pre2.metric(
        label="Investment Bounderies",
        value=result_GUI_settings_dict["input_premodeling_invest_boundaries"])
    if result_GUI_settings_dict["input_premodeling_invest_boundaries"]:
        pre3.metric(
            label="Tightening Factor",
            value=result_GUI_settings_dict
            ["input_premodeling_tightening_factor"])


def short_result_table(result_path_components):
    """
        Function to create tabel of components.
        :param result_path_components: path to a result components.csv file
        :type result_path_components: str
    """
    # Header
    st.subheader("Result Table")
    # Import components.csv and create dataframe
    df_components = pd.read_csv(result_path_components)
    # CSS to inject contained in a string
    hide_dataframe_row_index = """
                <style>
                .row_heading.level0 {display:none}
                .blank {display:none}
                </style>
                """

    # create table
    # set min hight which is the header height
    ag_min_height = 40
    # set right per row
    ag_row_height = 27.6
    # calculate logical height based on the df length
    logical_df_height = ag_min_height + len(df_components) * ag_row_height
    # set maximum height for st.AgGrid Table
    ag_max_height = 500

    # Inject CSS with Markdown
    st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

    # Creating st_aggrid table with setting the height to the min of the \
    # logical height or the max height
    AgGrid(df_components,
           fit_columns_on_grid_load=True,
           height=min(logical_df_height, ag_max_height))


def short_result_interactive_dia(result_path_results):
    """
        Function to create interactive results.

        :param result_path_results: path to a result results.csv file
        :type result_path_results: str
    """
    # Header
    st.subheader("Interactive Results")
    # loading result.csv as a dataframe
    result_df = pd.read_csv(result_path_results)
    # creating column headers to select
    column_headers_result = list(result_df.columns.values)
    # column headers without date
    list_headers = column_headers_result[1:]
    # selecting headers
    select_headers = st.multiselect("Select a bus:", list_headers)
    # filtered dataframe
    filtered_df = result_df[select_headers]
    # plotting
    fig = px.line(filtered_df).update_layout(
        xaxis_title="timestep (hour)",
        yaxis_title="performance (kW) / storage capacity (kWh)")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def create_energy_amounts_diagram(result_path_amounts):
    """
        Function to create energy amount diagrams in streamlit.

        :param result_path_amounts: path to a result heat_amounts.csv or \
            elec_amounts.csv file
        :type result_path_amounts: str
    """
    # loading result.csv as a dataframe
    amounts_df = pd.read_csv(result_path_amounts)
    amounts_df = amounts_df.loc[:, (amounts_df != 0).any(axis=0)]

    # creating column headers to select
    column_headers_amount = list(amounts_df.columns.values)
    # column headers without date
    list_headers = column_headers_amount[1:]

    # create plotly chart
    fig = px.area(amounts_df, x="run", y=list_headers).update_layout(
        xaxis_title="Reduced GHG-emissions compared to the cost minimum (%)",
        yaxis_title="energy amounts (kWh)")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def show_energy_amounts(result_path_heat_amounts, result_path_elec_amounts):
    """
        Function to create heat amounts.

        :param result_path_heat_amounts: path to a result heat_amounts.csv file
        :type result_path_heat_amounts: str
        :param result_path_elec_amounts: path to a result elec_amounts.csv file
        :type result_path_elec_amounts: str
    """
    # Header
    st.subheader("Energy Amount Diagrams")

    with st.subheader("Energy Amounts"):
        tab1, tab2 = st.tabs(["Heat Amounts", "Electricity Amounts"])
        # TODO: fix displayed amounts!
        # create heat amount diagram
        with tab1:
            create_energy_amounts_diagram(
                result_path_amounts=result_path_heat_amounts)
        # create elec amount diagram
        with tab2:
            create_energy_amounts_diagram(
                result_path_amounts=result_path_elec_amounts)

    # comment that diagrams are not always valid / can be wrong
    st.write("Info: The energy amount diagrams are only valid if the model \
             definition created with the Urban Upscaling Tool. \
             Otherwise there is no guarantee that there are no components \
             missing in the diagrams.")


def show_pareto(result_path_pareto):
    """
        Function to create heat amounts.

        :param result_path_results: path to a result heat_amounts.csv file
        :type result_path_results: str
    """
    # Header
    st.subheader("Pareto Diagram")

    # load pareto.csv
    pareto_df = pd.read_csv(result_path_pareto)
    # create and show pareto plot incl. point values
    fig = px.line(pareto_df,
                  x="costs",
                  y="emissions",
                  markers=True,
                  hover_data=["costs", "emissions"],
                  labels={"costs": "costs (EUR / a)",
                          "emissions": "emissions (g CO<sub>2</sub> / a)"}
                  )
    fig.update_traces(textposition="top right")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def show_building_specific_results(result_path_building_specific):
    """
        Function to create heat amounts.

        :param result_path_results: path to a result heat_amounts.csv file
        :type result_path_results: str
    """
    # Header
    with st.expander("Building specific results"):
        df_building_specific_data = pd.read_csv(result_path_building_specific)

        tab1, tab2 = st.tabs(["🗃 Data", "📈 Chart"])
        with tab1:
            # show the dataframe
            st.write(df_building_specific_data)

        with tab2:
            # get the y values for the chart
            column_headers = list(df_building_specific_data.columns.values)
            # delete building column
            column_headers.pop(0)
            # building specific figure
            # todo filter due to label in order to reduce the number
            # of buildings
            fig = px.bar(df_building_specific_data,
                         x="Building", y=column_headers)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def short_result_graph(result_path_graph):
    """
        Function to display the energy systems structure in a streamlit
            expander.

        :param result_path_graph: path to a result graph.gv.png file
        :type result_path_graph: str
    """
    # Header
    st.subheader("Energy System Graph")
    # Importing and printing the energy system graph
    with st.expander("Show the structure of the modeled energy system"):
        es_graph = Image.open(result_path_graph, "r")
        st.image(es_graph)


# starting page functions
# initialize global page settings
st_settings_global()

# initialize session state  if no result paths are defined on main page
if "state_result_path" not in st.session_state:
    st.session_state["state_result_path"] = "not set"

# start sidebar functions
result_processing_sidebar()

# show introduction page if no result paths are not set
if st.session_state["state_result_path"] == "not set":
    read_markdown_document(
        document_path="docs/GUI_texts/results.md",
        folder_path=f'{"docs/images/manual/Results/*"}')

elif os.path.join(st.session_state["state_result_path"], "components.csv") \
        in glob.glob(st.session_state["state_result_path"] + "/*"):

    # show short result summaries time series information
    short_result_summary_time(
        result_path_summary=st.session_state["state_result_path"]
        + "/summary.csv")

    # check if GUI settings dict is in result folder
    if os.path.join(st.session_state["state_result_path"],
                    "GUI_st_run_settings.json") \
            in glob.glob(st.session_state["state_result_path"] + "/*"):
        # import json as in a dict
        GUI_run_settings_dict = import_GUI_input_values_json(
            json_file_path=st.session_state["state_result_path"]
            + "/GUI_st_run_settings.json")
        # display some GUI settings if pre-modelling was active
        if GUI_run_settings_dict["input_timeseries_algorithm"] != "None":
            # show time series simplification settings
            short_result_simplifications(
                result_GUI_settings_dict=GUI_run_settings_dict)
        if GUI_run_settings_dict["input_activate_premodeling"]:
            # show time series simplification settings
            short_result_premodelling(
                result_GUI_settings_dict=GUI_run_settings_dict)
    # show short result summaries key values
    short_result_summary_system(
        result_path_summary=st.session_state["state_result_path"]
        + "/summary.csv")

    # show energy system graph
    short_result_graph(
        result_path_graph=st.session_state["state_result_path"]
        + "/graph.gv.png")
    # show components table
    short_result_table(
        result_path_components=st.session_state["state_result_path"]
        + "/components.csv")
    # show interactive result diagram
    short_result_interactive_dia(
        result_path_results=st.session_state["state_result_path"]
        + "/results.csv")


elif os.path.join(st.session_state["state_result_path"], "components.csv") \
        not in glob.glob(st.session_state["state_result_path"] + "/*"):
    # show building specific results
    show_pareto(
        result_path_pareto=os.path.join(st.session_state["state_result_path"],
                                        "pareto.csv"))
    # show heat amount diagram
    show_energy_amounts(
        result_path_heat_amounts=st.session_state["state_result_path"]
        + "/heat_amounts.csv",
        result_path_elec_amounts=st.session_state["state_result_path"]
        + "/elec_amounts.csv")
    # TODO implement
    # show building specific results
    # show_building_specific_results(st.session_state["state_result_path"]
    # + "/???????????.csv")

    # open short results for the chosen pareto point incl. header
    st.subheader("Short Results for Pareto Point: " +
                 st.session_state["state_pareto_point_chosen"])
    # show short result summaries time series informations
    short_result_summary_time(
        result_path_summary=st.session_state["state_pareto_result_path"]
        + "/summary.csv")
    # check if GUI settings dict is in result folder
    if os.path.join(st.session_state["state_pareto_result_path"],
                    "GUI_st_run_settings.json") \
            in glob.glob(st.session_state["state_pareto_result_path"] + "/*"):
        # import json as in a dict
        GUI_run_settings_dict = import_GUI_input_values_json(
            json_file_path=os.path.join(
                st.session_state["state_pareto_result_path"],
                "GUI_st_run_settings.json"))
        # display some GUI settings if pre-modelling was active
        if GUI_run_settings_dict["input_timeseries_algorithm"] != "None":
            # show time series simplification settings
            short_result_simplifications(
                result_GUI_settings_dict=GUI_run_settings_dict)
        if GUI_run_settings_dict["input_activate_premodeling"]:
            # show time series simplification settings
            short_result_premodelling(
                result_GUI_settings_dict=GUI_run_settings_dict)
    # show short result summaries key values
    short_result_summary_system(
        result_path_summary=st.session_state["state_pareto_result_path"]
        + "/summary.csv")
    # show components table
    short_result_table(
        result_path_components=st.session_state["state_pareto_result_path"]
        + "/components.csv")
    # show interactive result diagram
    short_result_interactive_dia(
        result_path_results=st.session_state["state_pareto_result_path"]
        + "/results.csv")
    # show energy system graph
    short_result_graph(
        result_path_graph=st.session_state["state_pareto_result_path"]
        + "/graph.gv.png")
