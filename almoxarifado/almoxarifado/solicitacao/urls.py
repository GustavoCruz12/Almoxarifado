from django.urls import path

from . import views

urlpatterns = [
    # usuario
    path('usuario/nova/', views.SolicitacaoCreate.as_view(), name='novaSolicitacao'),
    path('usuario/lista/', views.SolicitacaoList.as_view(), name='listaSolicitacao'),
    path('usuario/detalhes/<int:pk>', views.SolicitacaoDetail.as_view(), name='detalheSolicitacao'),
    path('usuario/deletar/<int:pk>', views.SolicitacaoDelete.as_view(), name='deleteSolicitacao'),
    #responsavel
    path('responsavel/lista/', views.SolicitacaoSecretarioList.as_view(), name='listaResponsavel'),
    #administrativo
    path('administrativo/lista/', views.SolicitacaoAdminstrativoList.as_view(), name='listaAdministrativo'),
    path('administrativo/lista/detalhe/<int:pk>', views.SolicitacaoAdministrativoDetail.as_view(), name='detalheAdministrativo'),
    path('administrativo/lista/detalhe/aprovacao/<int:pk>', views.SolicitacaoCreateUpdate.as_view(), name='createAdministrativo'),

    path('administrativo/entrega/lista/', views.SolicitacaoListEntrega.as_view(), name='entregaLista'),
    path('administrativo/entrega/lista/detalhes/<int:pk>', views.SolicitacaoDetailEntrega.as_view(), name='entregaDetalhe'),
    path('administrativo/entrega/detalhe/separacao_e_entrega/<int:pk>', views.SolicitacaoCreateEntrega.as_view(), name='entregaUpdate'),

    # materiais
    path('administrativo/materiais/novo', views.MateriaisCreate.as_view(), name='materiaiscreate'),
    path('administrativo/materiais/lista', views.MateriaisList.as_view(), name='materiaislist'),


    #secretario
    path('secretario/lista', views.SolicitacaoSecretarioList.as_view(), name='secretarioLista'),
    path('secretario/lista/detalhe/<int:pk>', views.SolicitacaoSecretarioDetail.as_view(), name='secretarioDetail'),
    path('secretario/lista/detalhe/aprovacao/<int:pk>', views.SolicitacaoSecretarioUpdate.as_view(), name='secretarioUpdate'),

    path('usuario/create', views.UsuarioCreate.as_view(), name='usuarioCreate')
    
]



 