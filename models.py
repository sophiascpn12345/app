import uuid
from django.db import models
from django.utils import timezone

class ProjectInfo(models.Model):
    project_code = models.CharField(max_length=100, verbose_name="项目编号")
    opportunity_number = models.CharField(max_length=100, verbose_name="商机编号")
    client_info = models.CharField(max_length=200, verbose_name="客户信息")
    product_info = models.CharField(max_length=200, verbose_name="产品简述")
    username = models.CharField(max_length=50, verbose_name="用户名")
    created_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        verbose_name = "项目信息"
        verbose_name_plural = "项目信息"

    def __str__(self):
        return self.project_code

class PCBBoard(models.Model):
    board_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    board_name = models.CharField(max_length=200, verbose_name="板卡名称")
    pcbManufacturer = models.CharField(max_length=200, verbose_name="三防厂家选择", blank=True)
    coatingManufacturer = models.CharField(max_length=200, verbose_name="PCB厂家选择", default='北京同力恒业')
    conformal_coating = models.CharField(verbose_name="三防涂覆", max_length=50, default='否', unique=False)

    pcb_layers = models.PositiveIntegerField(verbose_name="PCB 层数", null=True, blank=True)
    pcb_length = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="PCB长度(cm)", null=True, blank=True)
    pcb_width = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="PCB宽度(cm)", null=True, blank=True)
    pcb_quantity = models.PositiveIntegerField(verbose_name="PCB 数量", null=True, blank=True)
    pcb_unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单张PCB均价", null=True, blank=True)

    pcb_surface_process = models.CharField(max_length=200, verbose_name="表面工艺", blank=True)
    pcb_inspection_standard = models.CharField(max_length=200, verbose_name="检验标准", blank=True)
    pcb_engineering_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="工程费", null=True, blank=True)
    pcb_total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="PCB 总费用", null=True, blank=True)

    conformal_coating_unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单张三防均价", null=True, blank=True)
    conformal_coating_total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="三防总费用", null=True, blank=True)

    special_processes = models.CharField(max_length=200, verbose_name="特殊工艺", blank=True)
    username = models.CharField('用户名', max_length=50, null=True, blank=True, unique=False)
    createdTime = models.DateTimeField(verbose_name="创建时间", null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    pcbAndCoatingCost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="PCB加三防总费用", null=True, blank=True)

    class Meta:
        verbose_name = "PCB板卡信息"
        verbose_name_plural = "PCB板卡信息"

    def __str__(self):
        return f"{self.board_name} ({self.board_id})"

class Board(models.Model):
    project_info = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE, verbose_name="项目信息")
    board_name = models.CharField(max_length=200, verbose_name="板卡名称")
    board_size = models.CharField(max_length=50, verbose_name="板卡尺寸", blank=True)
    conformal_coating = models.BooleanField(verbose_name="是否三防", default=False)
    pcb_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="PCB成本", default=0)

    class Meta:
        verbose_name = "板卡信息"
        verbose_name_plural = "板卡信息"

    def __str__(self):
        return self.board_name

class Module(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name="所属板卡")
    type = models.CharField(max_length=100, verbose_name="模块类型")
    origin = models.CharField(max_length=100, verbose_name="模块产地")
    level = models.CharField(max_length=50, verbose_name="模块等级")
    quantity = models.PositiveIntegerField(verbose_name="模块数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="模块单价")

    class Meta:
        verbose_name = "模块信息"
        verbose_name_plural = "模块信息"

    def __str__(self):
        return f"{self.type} ({self.board.board_name})"