# 慢光工作室週報契約
只讀 input/tasks.csv 與 input/notes.md；不改來源。
開始前檢查 output/actions.csv、output/report.md、output/README.md；任何目標存在（含目錄或符號連結）即停止回報，不自行覆寫、刪除或另名。
只有本次已確認三個目標皆不存在而開始的新執行，才允許修正本次剛建立的輸出；中斷後重新啟動視為新執行，不接管部分舊成果。
重跑必須由人另建未使用的新一期資料夾，保存當期 input 來源快照、task-spec.md 與 verify.py；output 從空目錄開始，不更改舊一期。
README 必須交代上述重跑與停止規則，以及本期來源快照位置；不是在舊資料夾再跑一次。
只列 status 為 doing 或 todo 的工作；未知狀態必須停止回報。
輸出 output/actions.csv，維持來源順序；欄位固定：id,task,owner,due,status,sources。
空白 owner 寫「待確認」；空白 due 寫「待確認」。
不得把未批准的建議日期變成正式期限，不估算逾期。
sources 必須是 tasks.csv:ID;notes.md:ID，保留對應來源識別。
另輸出 output/report.md，使用二級標題「本週待辦」「待確認」「來源」。
G03 負責人與 G04 期限必須明列待確認，說明建議尚未批准。
另輸出 output/README.md，列重跑方法、驗收命令及目前限制。
輸出僅為本機草稿，不寄信、不發布、不設定排程、不保存技能。
完成後必須實際執行驗收，失敗則修正或標示阻礙。