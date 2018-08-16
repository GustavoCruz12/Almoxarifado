from django.urls import path

from . import views

urlpatterns = [
    # usuario
    path('nova/', views.SolicitacaoCreate.as_view(), name='novaSolicitacao'),
    path('lista/', views.SolicitacaoList.as_view(), name='listaSolicitacao'),
    path('detalhes/<int:pk>', views.SolicitacaoDetail.as_view(), name='detalheSolicitacao'),
    path('deletar/<int:pk>', views.SolicitacaoDelete.as_view(), name='deleteSolicitacao'),
    #responsavel
    path('lista/responsavel/', views.SolicitacaoSecretarioList.as_view(), name='listaResponsavel'),
    #administrativo
    path('lista/administrativo/', views.SolicitacaoAdminstrativoList.as_view(), name='listaAdministrativo'),
    path('detail/administrativo/<int:pk>', views.SolicitacaoAdministrativoDetail.as_view(), name='detalheAdministrativo'),
    path('create/administrativo/<int:pk>', views.SolicitacaoAdminstrativoUpdate.as_view(), name='createAdministrativo'),

]



