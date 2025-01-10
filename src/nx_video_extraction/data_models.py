from datetime import datetime as dt
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class NxParams(BaseModel):
    username: str
    password: str


class TokenNX(BaseModel):
    token: str


class Quality (str, Enum):
    hi = "hi"
    lo = "lo"


class RecordData(BaseModel):
    camera_id: str
    start: str
    duration: int
    quality: Quality
    path: str


class Ticket(BaseModel):
    id: int
    employeeId: int = 1
    storeId: int = 1
    totalIssues: int = 0
    issueRate: float = 0
    totalItems: int = 0
    hasIssues: bool = False
    issueTypes: List[str] = None
    status: str = 'Open'
    notes: str = ''
    lossValue: float = 0
    initDatetime: str = dt.now().isoformat()
    endDatetime: str = dt.now().isoformat()
    duration: int = 0
    posId: str = 'pos-1'
    cameraId: str = ''
    serverIP: str = '0.0.0.0'
    videoPath: str = None
    superOrganizationId: str = ''
    organizationId: str = ''


class Item(BaseModel):
    id: int
    sku: str = ''
    description: str = ''
    price: float = None
    units: float = None
    predictedCategory: str = ''
    categoryScore: float = None
    predictedProduct: str = ''
    productScore: float = None
    initDatetime: str = dt.now().isoformat()
    endDatetime: str = dt.now().isoformat()
    duration: int = 0
    hasIssue: bool = False
    issueScore: float = None
    issueType: str = None
    revisionType: str = ''
    status: str = 'Open'
    ticketId: int
    # cameraId: str = ''