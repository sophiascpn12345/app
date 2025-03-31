import uuid
import decimal
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import ProjectInfo, PCBBoard, Board, Module
from django.views.decorators.csrf import csrf_exempt

# 假设的基准价和工程费字典
pcbProjectFeeDic = {2: 100, 4: 200, 6: 300, 8: 400, 10: 500, 12: 600, 14: 700, 16: 800, 18: 900, 20: 1000}
pcbBasePriceDic = {
    '2-0': 0.1, '2-1': 0.2, '2-3': 0.3, '2-10': 0.4, '2-20': 0.5, '2-50': 0.6, '2-100': 0.7,
    '4-0': 0.2, '4-1': 0.3, '4-3': 0.4, '4-10': 0.5, '4-20': 0.6, '4-50': 0.7, '4-100': 0.8,
    # 其他层数的基准价可以继续添加
}

def evaluateMainPage(request):
    return render(request, 'costApp/evaluateMainPage.html')

def projectInfo(request):
    if request.method == 'GET':
        username = request.session.get('username')
        return render(request, "costApp/projectInfo.html", {'username': username})
    elif request.method == 'POST':
        project_code = request.POST.get('projectCode')
        opportunity_number = request.POST.get('opportunityNumber')
        client_info = request.POST.get('clientInfo')
        product_info = request.POST.get('productInfo')
        username = request.session.get('username')
        created_time = timezone.now()

        ProjectInfo.objects.create(
            project_code=project_code,
            opportunity_number=opportunity_number,
            client_info=client_info,
            product_info=product_info,
            username=username,
            created_time=created_time
        )
        return redirect('metaInstrumentsCostEvaluate')

def metaInstrumentsCostEvaluate(request):
    if request.method == 'GET':
        try:
            inst = ProjectInfo.objects.filter(username=request.session['username']).latest('id')
        except ProjectInfo.DoesNotExist:
            inst = None
        boards = []
        fillDate = timezone.now().date()
        username = request.session.get('username')
        return render(request, 'costApp/metaInstrumentsCostEvaluate.html', locals())
    elif request.method == 'POST':
        projectId = request.POST.get('projectId')
        businessId = request.POST.get('businessId')
        reportDate = request.POST.get('reportDate')
        operator = request.POST.get('operator')
        productName = request.POST.get('productName')

        project_info = ProjectInfo(
            projectId=projectId,
            businessId=businessId,
            reportDate=reportDate,
            operator=operator,
            productName=productName
        )
        project_info.save()

        board_index = 1
        while True:
            board_name_key = f'board_name_{board_index}'
            if board_name_key in request.POST:
                board_name = request.POST[board_name_key]
                board = Board(name=board_name, project_info=project_info)
                board.save()

                module_index = 1
                while True:
                    module_name_key = f'module_name_{board_index}_{module_index}'
                    if module_name_key in request.POST:
                        module_name = request.POST[module_name_key]
                        module_localization = request.POST.get(f'module_localization_{board_index}_{module_index}')
                        module_level = request.POST.get(f'module_level_{board_index}_{module_index}')
                        module_quantity = request.POST.get(f'module_quantity_{board_index}_{module_index}')
                        module_price = request.POST.get(f'module_price_{board_index}_{module_index}')

                        module = Module(
                            name=module_name,
                            localization=module_localization,
                            level=module_level,
                            quantity=module_quantity,
                            price=module_price,
                            board=board
                        )
                        module.save()
                        module_index += 1
                    else:
                        break

                board_index += 1
            else:
                break

        return redirect('componentCostEvaluateSummery')

@csrf_exempt
def pcbCostEvaluate(request):
    if request.method == 'POST':
        try:
            board_id = request.POST.get('boardId')
            board_name = request.POST.get('board_name')
            conformal_coating = request.POST.get('conformal_coating', '否')
            pcb_layers = int(request.POST.get('pcb_layers', 2))
            pcb_length = decimal.Decimal(request.POST.get('pcb_length', 0))
            pcb_width = decimal.Decimal(request.POST.get('pcb_width', 0))
            pcb_quantity = int(request.POST.get('pcb_quantity', 0))
            special_processes = request.POST.get('special_processes_str', '')

            PCBBoardDic = {}
            PCBBoardDic['board_name'] = board_name
            PCBBoardDic['conformal_coating'] = conformal_coating
            PCBBoardDic['pcbManufacturer'] = request.POST.get('pcbManufacturer', None)
            PCBBoardDic['coatingManufacturer'] = request.POST.get('coatingManufacturer', None)
            PCBBoardDic['pcb_layers'] = pcb_layers
            PCBBoardDic['pcb_length'] = pcb_length
            PCBBoardDic['pcb_width'] = pcb_width
            PCBBoardDic['pcb_quantity'] = pcb_quantity
            PCBBoardDic['pcb_surface_process'] = request.POST.get('pcb_surface_process', '')
            PCBBoardDic['pcb_inspection_standard'] = request.POST.get('pcb_inspection_standard', '')
            PCBBoardDic['special_processes'] = special_processes

            pcb_engineering_fee = pcbProjectFeeDic[pcb_layers]
            areaCm = float(pcb_length) * float(pcb_width) * float(pcb_quantity)
            area = areaCm / 10000
            pcbSurfacePrice = 0
            if area > 100:
                pcbBasePriceKey = str(pcb_layers) + '-100'
            elif area > 50:
                pcbBasePriceKey = str(pcb_layers) + '-50'
            elif area > 20:
                pcbBasePriceKey = str(pcb_layers) + '-20'
            elif area > 10:
                pcbBasePriceKey = str(pcb_layers) + '-10'
            elif area > 3:
                pcbBasePriceKey = str(pcb_layers) + '-3'
            elif area > 1:
                pcbBasePriceKey = str(pcb_layers) + '-1'
            else:
                pcbBasePriceKey = str(pcb_layers) + '-0'

            if PCBBoardDic['pcb_surface_process'] == '沉金':
                pcbSurfacePrice = 0.02
            baseCostPrice = pcbBasePriceDic[pcbBasePriceKey] * areaCm + pcbSurfacePrice * (int(areaCm) + 1)

            addedItems = 0
            verifyItem = 0
            orderItem = 0
            specialItem = 0

            if 2 <= pcb_layers <= 8:
                addedItems = 0.25
            elif 10 <= pcb_layers <= 20:
                addedItems = 0.2

            if PCBBoardDic['pcb_inspection_standard'] == 'IPC3级':
                verifyItem = 0.1
            elif PCBBoardDic['pcb_inspection_standard'] == '军工':
                verifyItem = 0.3
            elif PCBBoardDic['pcb_inspection_standard'] == '医疗产品':
                verifyItem = 0.1

            if pcb_quantity < 20:
                orderItem = 100
            elif pcb_quantity >= 20:
                orderItem = pcb_quantity * 5

            if '金手指' in special_processes:
                specialItem = 700
            if '背钻' in special_processes:
                specialItem = specialItem + 200 * 3
            if '树脂塞孔' in special_processes:
                specialItem = specialItem + 300 * (int(area) + 1)
            if '盘中孔' in special_processes:
                specialItem = specialItem + 300 * (int(area) + 1)

            pcb_total_cost = round(
                pcb_engineering_fee + baseCostPrice * (1 + addedItems + verifyItem) + orderItem + specialItem, 2)

            PCBBoardDic['pcb_total_cost'] = pcb_total_cost
            PCBBoardDic['pcb_engineering_fee'] = pcb_engineering_fee
            pcb_unit_price = round(pcb_total_cost / pcb_quantity, 2)
            PCBBoardDic['pcb_unit_price'] = pcb_unit_price
            conformal_coating_unit_price = 300
            PCBBoardDic['conformal_coating_unit_price'] = conformal_coating_unit_price
            conformal_coating_total_cost = 300 * pcb_quantity
            PCBBoardDic['conformal_coating_total_cost'] = conformal_coating_total_cost
            PCBBoardDic['pcbAndCoatingCost'] = pcb_total_cost + conformal_coating_total_cost

            PCBBoardDic['username'] = request.session.get('username')
            PCBBoardDic['createdTime'] = timezone.now()

            board, created = PCBBoard.objects.update_or_create(
                board_id=board_id,
                defaults=PCBBoardDic
            )

            return JsonResponse({
                'success': True,
                'board_name': board_name,
                'pcb_layers': pcb_layers,
                'pcb_length': float(pcb_length),
                'pcb_width': float(pcb_width),
                'pcb_quantity': pcb_quantity,
                'pcb_surface_process': PCBBoardDic['pcb_surface_process'],
                'pcb_inspection_standard': PCBBoardDic['pcb_inspection_standard'],
                'conformal_coating': conformal_coating,
                'pcb_unit_price': float(pcb_unit_price),
                'pcb_engineering_fee': float(pcb_engineering_fee),
                'pcb_total_cost': float(pcb_total_cost),
                'conformal_coating_unit_price': float(conformal_coating_unit_price),
                'conformal_coating_total_cost': float(conformal_coating_total_cost),
                'pcbAndCoatingCost': float(PCBBoardDic['pcbAndCoatingCost'])
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    elif request.method == 'GET':
        urlParams = request.GET
        boardId = urlParams.get('boardId')
        if boardId:
            try:
                board = PCBBoard.objects.get(board_id=boardId)
                data = {
                    'success': True,
                    'board_name': board.board_name,
                    'pcbManufacturer': board.pcbManufacturer,
                    'coatingManufacturer': board.coatingManufacturer,
                    'conformal_coating': board.conformal_coating,
                    'pcb_layers': board.pcb_layers,
                    'pcb_length': float(board.pcb_length) if board.pcb_length else None,
                    'pcb_width': float(board.pcb_width) if board.pcb_width else None,
                    'pcb