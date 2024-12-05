<%@ page language="java" contentType="text/html; charset=EUC-KR"
    pageEncoding="EUC-KR"%>

<%@ include file="/jsp/common/SessionCheck.jsp" %>
<%@ include file="/jsp/common/Logger.jsp" %>

<jsp:useBean id="sr0300Bean" class="swis.bean.biz.sr0300Bean"/>
<jsp:setProperty property="*" name="sr0300Bean" />

<html>
<head>
<!-- <meta http-equiv="Content-Type" content="text/html; charset=EUC-KR"> -->
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<link rel="stylesheet" type="text/css" href="/css/base.css"/>
<link rel="stylesheet" type="text/css" media="screen" href="/css/jqueryUi/jquery-ui.min.css"/>
<link rel="stylesheet" type="text/css" media="screen" href="/css/jqueryUi/ui.jqgrid.css"/>
<script src="/js/jquery-1.11.0.min.js"   type="text/javascript"></script>
<script src="/js/cal/jquery.min.js"   type="text/javascript"></script>
<script src="/js/cal/jquery-ui.min.js"   type="text/javascript"></script>
<script src="/js/i18n/grid.locale-kr.js" type="text/javascript"></script>
<script src="/js/jquery.jqGrid.min.js"   type="text/javascript"></script>
<script type=text/javascript src=/js/checkMainFrame.js></script>

<script type=text/javascript>
function onKeyDown(e)
{
	e.which = e.which || e.keyCode;
	if(e.which == 13)
			onQueryClicked();
}
$(document).ready(function(){
	
	$("#schPrdFrom").datepicker({
	    changeMonth: true,
	    changeYear: true,
	    dateFormat:'yy-mm-dd'
	});
	$("#schPrdTo").datepicker({
	    changeMonth: true,
	    changeYear: true,
	    dateFormat:'yy-mm-dd'
	});
	
	//�����˾�
	$("#scrtAcNo").dblclick(function(){  
    	var win = window.open("/swis/jsp/biz/cm0010.jsp", "new_message", "width=545px,height=460px,left=100,top=100,status=no,location=no,menubar=no,resizable=no,scrollbars=no,titlebar=no,toolbar=no,directories=no");		
    	win.focus();
	});
	
});

//�����˾����ð� ����
function setAcVal(acNo,acNm){
	conditionForm.scrtAcNo.value = acNo;
	conditionForm.scrtAcn.value  = acNm;	
}

function onQueryClicked()
{
	listFrame.document.listForm.trCode.value        = "Q";
	listFrame.document.listForm.scrtAcNo.value      = conditionForm.scrtAcNo.value;
	listFrame.document.listForm.trnsRsn.value       = conditionForm.trnsRsn.value;
	listFrame.document.listForm.currCd.value        = conditionForm.currCd.value;
	listFrame.document.listForm.pgsStus.value       = conditionForm.pgsStus.value;
	//listFrame.document.listForm.dDv.value           = conditionForm.dDv.value;
	listFrame.document.listForm.dDv.value           = "A";
	listFrame.document.listForm.schPrdFrom.value    = conditionForm.schPrdFrom.value;
	listFrame.document.listForm.schPrdTo.value      = conditionForm.schPrdTo.value;
	
	listFrame.document.listForm.submit();
}
</script>

</head>
<body onload="checkMainFrame();">

<table><tr><td>
<table style="width:400px;height:30px;font-size:15px;color:#149" background="/img/title_back.jpg">
<tr><td width=25>&nbsp;</td><td><b>Transfer</b></td></tr>
</table>
</td></tr></table>

<%
	sr0300Bean.setRequest(request);
	sr0300Bean.setSession(session);
	sr0300Bean.setLogger(logger);
	
	sr0300Bean.validate();
%>

<form name=conditionForm method=post>
	<input type=hidden name=trCode>
	<!--��ȸ���� ����-->
	<div class="application_inquiry1">
		<table border="1" cellspacing="0" cellpadding="0" class="table03" style="font-size:12px">
			<tbody>
				<tr>
					<td width=100 class=th0>&nbsp;<img width=5 height=5 src="/img/box.jpg">&nbsp;account no.</td>
					<td width=300><input type=text id='scrtAcNo' name='scrtAcNo' maxlength=15 value="<%=sr0300Bean.getScrtAcNo()%>" style="width:100px;font-size:12px;border:1px solid gray" onkeydown="onKeyDown(event)">
					              <input type=text id='scrtAcn'  name='scrtAcn'  maxlength=50 value="<%=sr0300Bean.getScrtAcn()%>"  readonly style="width:140px;border:1px solid gray;background:#e0e0e0">
					</td>
					<td width=100 class=th0>&nbsp;<img width=5 height=5 src="/img/box.jpg">&nbsp;transfer type</td>
					<td width=200>
						<select name=trnsRsn style="width:70px;font-size:12px">
			<%
						String[] trnsRsnN	= sr0300Bean.getTrnsRsnN();
						String[] trnsRsnV	= sr0300Bean.getTrnsRsnV();
						String   trnsRsn	= sr0300Bean.getTrnsRsn();
			
						for(int i = 0;i < trnsRsnN.length;i ++)
						{
			%>
							<option value=<%=trnsRsnV[i]%>><%=trnsRsnN[i]%>
			<%
						}
			%>
						</select>
					</td>
				</tr>
				<tr>
					<td width=100 class=th0>&nbsp;<img width=5 height=5 src="/img/box.jpg">&nbsp;currency</td>
					<td width=250>
						<select name=currCd style="width:70px;font-size:12px">
			<%
						String[] currN		= sr0300Bean.getCurrN();
						String[] currV		= sr0300Bean.getCurrV();
						String   curr		= sr0300Bean.getCurr();
			
						for(int i = 0;i < currN.length;i ++)
						{
			%>
							<option value=<%=currV[i]%>><%=currN[i]%>
			<%
						}
			%>
						</select>
					</td>
					
					<td width=100 class=th0>&nbsp;<img width=5 height=5 src="/img/box.jpg">&nbsp;progress stat.</td>
					<td width=200>
						<select name=pgsStus style="width:100px;font-size:12px">
			<%
						String[] pgsStusN		= sr0300Bean.getPgsStusN();
						String[] pgsStusV		= sr0300Bean.getPgsStusV();
						String   pgsStus		= sr0300Bean.getPgsStus();
			
						for(int i = 0;i < pgsStusN.length;i ++)
						{
			%>
							<option value=<%=pgsStusV[i]%>><%=pgsStusN[i]%>
			<%
						}
			%>
						</select>
					</td>
				</tr>
				<tr>
					<td width=100 class=th0>&nbsp;<img width=5 height=5 src="/img/box.jpg">&nbsp;date</td>
					<td width=250 colspan='3'>
						<!-- select name=dDv style="font-size:12px">
			<%
						String[] dDvN		= sr0300Bean.getDDvN();
						String[] dDvV		= sr0300Bean.getDDvV();
						String   dDv		= sr0300Bean.getDDv();
			
						for(int i = 0;i < dDvN.length;i ++)
						{
			%>
							<option value=<%=dDvV[i]%>><%=dDvN[i]%>
			<%
						}
			%>
						</select-->
						<input type='text' id='schPrdFrom' name='schPrdFrom' maxlength=10 value="<%=sr0300Bean.getSchPrdFrom()%>" style="width:70px;font-size:12px;border:1px solid gray" onkeydown="onKeyDown(event)"> ~
						<input type='text' id='schPrdTo'   name='schPrdTo'   maxlength=10 value="<%=sr0300Bean.getSchPrdTo()%>"   style="width:70px;font-size:12px;border:1px solid gray" onkeydown="onKeyDown(event)"></td>					
				</tr>
				<tr><td colspan=4 align=right>
	  			<a href="javascript:onQueryClicked()"><img src="/img/btn_inquiry.jpg" border=0 alt="query" id="searchBtn"/></a>
				</td></tr>
			</tbody>
		</table>
	</div>			
		

</form>

<div>
	<iframe name=listFrame src="/swis/jsp/biz/sr0301.jsp" width=1050 height=450 frameborder=0 border=0 marginheight=1 marginwidth=1 cellpadding=0 cellspacing=0></iframe>
</div>

</body>
</html>
