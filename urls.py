from django.urls import path
from . import views


urlpatterns = [
    path('evaluateMainPage', views.evaluateMainPage),
    path('metaMaterialCostEvaluate', views.metaMaterialCostEvaluate),
    path('pcbMaterialCostEvaluate', views.pcbMaterialCostEvaluate),
    #path('metaInstrumentsCostEvaluate', views.metaInstrumentsCostEvaluate,name='metaInstrumentsCostEvaluate'),
    path('projectInfo/', views.project_info, name='project_info'),
    path('save_project_info/', views.save_project_info, name='save_project_info'),
    path('metaInstrumentsCostEvaluate/<int:project_id>/', views.meta_instruments_cost_evaluate, name='meta_instruments_cost_evaluate'),
    path('save_meta_instruments/', views.save_meta_instruments, name='save_meta_instruments'),

    path('componentCostEvaluateSummery',views.componentCostEvaluateSummery),
    path('structureCostEvaluate', views.structureCostEvaluate),
    #path('pcbCostEvaluate', views.pcbCostEvaluate, name='pcb_cost_evaluate'),
    path('save_pcb/', views.save_pcb, name='save_pcb'),
    path('get_pcb_data/', views.get_pcb_data, name='get_pcb_data'),
    ]
'''
urlpatterns = [
    path('evaluateMainPage', views.evaluateMainPage),
    path('projectInfo/', views.project_info, name='project_info'),
    path('metaInstrumentsCostEvaluate/<int:project_id>/', views.meta_instruments_cost_evaluate, name='meta_instruments_cost_evaluate'),
    path('pcbCostEvaluate/', views.pcb_cost_evaluate, name='pcb_cost_evaluate'),
    path('save_meta_instruments/', views.save_meta_instruments, name='save_meta_instruments'),
    path('componentCostEvaluateSummery/', views.component_cost_evaluate_summery, name='component_cost_evaluate_summery'),
]
'''