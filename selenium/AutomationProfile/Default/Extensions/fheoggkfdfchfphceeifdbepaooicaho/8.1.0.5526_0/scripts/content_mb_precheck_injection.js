/*!
 * 
 *     MCAFEE RESTRICTED CONFIDENTIAL
 *     Copyright (c) 2024 McAfee, LLC
 *
 *     The source code contained or described herein and all documents related
 *     to the source code ("Material") are owned by McAfee or its
 *     suppliers or licensors. Title to the Material remains with McAfee
 *     or its suppliers and licensors. The Material contains trade
 *     secrets and proprietary and confidential information of McAfee or its
 *     suppliers and licensors. The Material is protected by worldwide copyright
 *     and trade secret laws and treaty provisions. No part of the Material may
 *     be used, copied, reproduced, modified, published, uploaded, posted,
 *     transmitted, distributed, or disclosed in any way without McAfee's prior
 *     express written permission.
 *
 *     No license under any patent, copyright, trade secret or other intellectual
 *     property right is granted to or conferred upon you by disclosure or
 *     delivery of the Materials, either expressly, by implication, inducement,
 *     estoppel or otherwise. Any license under such intellectual property rights
 *     must be expressed and approved by McAfee in writing.
 *
 */(()=>{"use strict";const e=0,s="PRINT_IN_BACKGROUND",o={NONE:0,INFO:1,ERROR:2,WARN:3,DEBUG:4,ALL_IN_BACKGROUND:99},t=1,r=2,c=3,n=4,a={BACKGROUND:"BACKGROUND",CONTENT:"CONTENT",TELEMETRY:"TELEMETRY"},i={DEFAULT:"color: #000000; font-weight: normal; font-style:normal; background: #FFFFFF;",BACKGROUND:"color: #8D0DBA; font-weight: bold; background: #FFFFFF;",CONTENT:"color: #F54A26; font-weight: bold; background: #FFFFFF;",TELEMETRY:"color: #147831; font-weight: bold; background: #FFFFFF;"};const l=new class{constructor(){this.storageChecked=!1,this.logLevel=null,this.queue=[];const s="MCLOGLEVEL";chrome?.storage?.local.get([s]).then((t=>{const r=Object.values(o).includes(t[s]);this.logLevel=r?t[s]:e,this.logLevel!==o.NONE&&this.queue.forEach((({callback:e,message:s,processType:o})=>{e(s,o)})),this.queue=[],this.storageChecked=!0}))}log(e,s=null){this.storageChecked?this.processLog(e,t,s,this.logLevel):this.queue.push({callback:this.log.bind(this),message:e,processType:s})}error(e,s=null){this.storageChecked?this.processLog(e,r,s,this.logLevel):this.queue.push({callback:this.error.bind(this),message:e,processType:s})}warn(e,s=null){this.storageChecked?this.processLog(e,c,s,this.logLevel):this.queue.push({callback:this.warn.bind(this),message:e,processType:s})}debug(e,s=null){this.storageChecked?this.processLog(e,n,s,this.logLevel):this.queue.push({callback:this.debug.bind(this),message:e,processType:s})}processLog(e,t,c,n){if(n===o.NONE)return;let i="chrome-extension:"===location.protocol?a.BACKGROUND:a.CONTENT;c&&a[c]&&(i=c);const l=new Date,h=t===r?e:`%c[${i} ${l.toLocaleString([],{hour:"2-digit",minute:"2-digit",second:"2-digit",hour12:!0})}]: %c${e}`;i===a.CONTENT&&this.logLevel===o.ALL_IN_BACKGROUND&&chrome.runtime.sendMessage({command:s,logMessage:h,processType:i,logType:t,logLevel:n}),this.printLog(h,i,t,n)}printLog(e,s,a,l){const h=i.DEFAULT,g=i[s]||h;if(l>=o.ERROR&&a===r&&console.error(e),l>=o.INFO&&a===t&&console.log(e,g,h),l>=o.WARN&&a===c){const s="color: #FFA500; font-family: sans-serif; font-weight: bolder; text-shadow: #000 1px 1px;";console.log(`%cWARN - ${e}`,s,g,h)}if(l>=o.DEBUG&&a===n){const s="color: #FF33D7; font-family: sans-serif; font-weight: bolder; text-shadow: #000 1px 1px;";console.log(`%cDEBUG - ${e}`,s,g,h)}}},h=async(e,s,o,t)=>{try{chrome.tabs.sendMessage(t,{ipcId:e,command:s,...o},{},(()=>{chrome.runtime.lastError}))}catch(e){l.warn(`[broadcast] Unexpected error when calling command: "${s}", err: ${e.message}`)}},g=(e,s,o,t,r=null)=>{if(!chrome.tabs)throw new Error('"tabs" permission not set in manifest.');const c={};return"number"==typeof r&&(c.frameId=r),chrome.tabs.sendMessage(t,{ipcId:e,command:s,...o},c)},d=(e,s={},o)=>(async(e,s,o={},t={})=>{try{if(t?.tabId){const{tabId:r,frameId:c}=t;return await g(e,s,o,r,c)}if(t?.broadcast){const r=await chrome.tabs.query({}),{broadcastIgnoreId:c=[]}=t;return r.filter((({id:e})=>!c.includes(e))).forEach((({id:t})=>{h(e,s,o,t)})),!0}return await chrome.runtime.sendMessage({ipcId:e,command:s,...o})}catch(e){return l.warn(`Unexpected error when calling command: "${s}", err: ${e.message}`),null}})("WA",e,s,o),u="MB_PRE_CHECK_INJECTION";(class{static start(){try{d(u)}catch(e){}}}).start()})();
//# sourceMappingURL=../sourceMap/chrome/scripts/content_mb_precheck_injection.js.map