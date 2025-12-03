import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# 异常低价警戒线计算程序
def calculate_alert_line(bid_prices, max_limit, float_value=None):
    """
    计算异常低价警戒线
    
    参数:
    - bid_prices: 所有报价列表
    - max_limit: 最高限价
    - float_value: 下浮值 (5%-10%)，默认随机
    """
    import random
    
    if float_value is None:
        float_value = random.uniform(0.05, 0.1)  # 5%-10%
    
    # 步骤1: 有效报价范围筛选
    # 剔除高于最高限价95%和低于最高限价78%的报价
    valid_prices = [p for p in bid_prices if 0.78 * max_limit <= p <= 0.95 * max_limit]
    
    if not valid_prices:
        return None, {}, float_value
    
    n = len(valid_prices)
    
    # 步骤2: 去掉上述范围内最低15%和最高10%的投标单位报价
    sorted_prices = sorted(valid_prices)
    low_cut = int(n * 0.15)  # 去掉最低15%
    high_cut = int(n * 0.10)  # 去掉最高10%
    
    if low_cut + high_cut >= n:
        # 如果去掉的太多，使用所有有效报价
        filtered_prices = valid_prices
    else:
        filtered_prices = sorted_prices[low_cut : n - high_cut]
    
    if not filtered_prices:
        filtered_prices = valid_prices
    
    # 步骤3: 计算综合平均数
    # 算术平均数
    arithmetic_mean = np.mean(filtered_prices)
    
    # 中位数平均数（就是中位数）
    median_mean = np.median(filtered_prices)
    
    # 四分位数平均数
    q1 = np.percentile(filtered_prices, 25)
    q3 = np.percentile(filtered_prices, 75)
    quartile_mean = (q1 + q3) / 2
    
    # 综合平均数
    if n < 5:
        comprehensive_mean = arithmetic_mean
    else:
        comprehensive_mean = (arithmetic_mean + median_mean + quartile_mean) / 3
    
    # 步骤4: 计算异常低价警戒线
    alert_line = comprehensive_mean * (1 - float_value)
    
    # 标记低于警戒线的报价
    below_alert = {}
    for price in bid_prices:
        below_alert[price] = price < alert_line
    
    # 收集中间结果
    intermediate = {
        'valid_prices': valid_prices,
        'filtered_prices': filtered_prices,
        'arithmetic_mean': arithmetic_mean,
        'median_mean': median_mean,
        'q1': q1,
        'q3': q3,
        'quartile_mean': quartile_mean,
        'comprehensive_mean': comprehensive_mean,
        'alert_line': alert_line,
        'below_alert': below_alert
    }
    
    return alert_line, intermediate, float_value


class AlertLineCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("异常低价警戒线计算器")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="异常低价警戒线计算器",
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 报价输入
        ttk.Label(main_frame, text="报价列表 (用逗号分隔):",
                 font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.bid_entry = ttk.Entry(main_frame, width=50)
        self.bid_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.bid_entry.insert(0, "850000,900000,950000,980000,1000000,1020000,1050000")
        
        # 最高限价
        ttk.Label(main_frame, text="最高限价:",
                 font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.max_limit_entry = ttk.Entry(main_frame)
        self.max_limit_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.max_limit_entry.insert(0, "1100000")
        
        # 参数设置
        param_frame = ttk.LabelFrame(main_frame, text="下浮值参数设置", padding="10")
        param_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        param_frame.columnconfigure(1, weight=1)
        
        ttk.Label(param_frame, text="下浮值设定方式:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.float_mode = tk.StringVar(value="range")
        mode_frame = ttk.Frame(param_frame)
        mode_frame.grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(mode_frame, text="指定范围（随机生成）", variable=self.float_mode, 
                       value="range", command=self.toggle_float_mode).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(mode_frame, text="固定值", variable=self.float_mode, 
                       value="fixed", command=self.toggle_float_mode).pack(side=tk.LEFT)
        
        # 范围输入
        self.range_frame = ttk.Frame(param_frame)
        self.range_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(self.range_frame, text="范围:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(self.range_frame, text="最小值:").pack(side=tk.LEFT, padx=(0, 5))
        self.float_min_entry = ttk.Entry(self.range_frame, width=10)
        self.float_min_entry.insert(0, "0.05")
        self.float_min_entry.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(self.range_frame, text="最大值:").pack(side=tk.LEFT, padx=(0, 5))
        self.float_max_entry = ttk.Entry(self.range_frame, width=10)
        self.float_max_entry.insert(0, "0.10")
        self.float_max_entry.pack(side=tk.LEFT)
        
        # 固定值输入
        self.fixed_frame = ttk.Frame(param_frame)
        self.fixed_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(self.fixed_frame, text="固定值:").pack(side=tk.LEFT, padx=(0, 5))
        self.float_fixed_entry = ttk.Entry(self.fixed_frame, width=15)
        self.float_fixed_entry.insert(0, "0.075")
        self.float_fixed_entry.pack(side=tk.LEFT)
        
        ttk.Label(param_frame, text="说明：下浮值越大，警戒线越低（例如：0.05表示下浮5%，0.10表示下浮10%）").grid(
            row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 2))
        
        # 按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="计算警戒线",
                  command=self.calculate).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="清空",
                  command=self.clear).grid(row=0, column=1, padx=5)
        
        # 结果显示
        result_frame = ttk.LabelFrame(main_frame, text="计算结果", padding="10")
        result_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        self.result_text = tk.Text(result_frame, height=20, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        main_frame.rowconfigure(5, weight=1)
        
        self.toggle_float_mode()
    
    def toggle_float_mode(self):
        """切换下浮值输入模式"""
        if self.float_mode.get() == "range":
            # 显示范围输入，隐藏固定值输入
            self.range_frame.grid()
            self.fixed_frame.grid_remove()
        else:
            # 显示固定值输入，隐藏范围输入
            self.range_frame.grid_remove()
            self.fixed_frame.grid()
    
    def calculate(self):
        try:
            # 获取输入
            bid_input = self.bid_entry.get().strip()
            if not bid_input:
                messagebox.showerror("输入错误", "请输入报价列表")
                return
            
            bid_prices = [float(p.strip()) for p in bid_input.split(',')]
            max_limit = float(self.max_limit_entry.get().strip())
            
            # 获取下浮值
            if self.float_mode.get() == "fixed":
                # 使用固定值
                float_value = float(self.float_fixed_entry.get())
                if not (0.05 <= float_value <= 0.1):
                    raise ValueError("下浮值必须在0.05-0.1之间")
            else:
                # 使用范围随机生成
                float_min = float(self.float_min_entry.get())
                float_max = float(self.float_max_entry.get())
                if float_min >= float_max:
                    raise ValueError("最小值必须小于最大值")
                if not (0.05 <= float_min <= 0.1) or not (0.05 <= float_max <= 0.1):
                    raise ValueError("下浮值范围必须在0.05-0.1之间")
                # 传入范围，让calculate_alert_line内部生成
                import random
                float_value = random.uniform(float_min, float_max)
            
            # 计算
            alert_line, intermediate, float_used = calculate_alert_line(
                bid_prices, max_limit, float_value
            )
            
            # 显示结果
            self.result_text.delete(1.0, tk.END)
            
            if alert_line is None:
                self.result_text.insert(tk.END, "错误：没有符合条件的有效报价\n")
                return
            
            self.result_text.insert(tk.END, "=== 异常低价警戒线计算过程 ===\n\n")
            
            # 1. 有效报价筛选
            valid_prices = intermediate['valid_prices']
            self.result_text.insert(tk.END, f"【步骤1】有效报价范围筛选\n")
            self.result_text.insert(tk.END, f"{'-'*70}\n")
            self.result_text.insert(tk.END, f"最高限价: {max_limit:.2f} 元\n")
            self.result_text.insert(tk.END, f"有效范围: {0.78*max_limit:.2f} 元 ~ {0.95*max_limit:.2f} 元\n")
            self.result_text.insert(tk.END, f"规则说明: 剔除高于最高限价95%和低于78%的报价\n")
            self.result_text.insert(tk.END, f"有效报价: {', '.join([f'{p:.0f}' for p in sorted(valid_prices)])}\n")
            self.result_text.insert(tk.END, f"有效报价数量: {len(valid_prices)} 家\n\n")
            
            # 2. 去掉高低报价
            filtered = intermediate['filtered_prices']
            n = len(valid_prices)
            self.result_text.insert(tk.END, f"【步骤2】排除高低报价\n")
            self.result_text.insert(tk.END, f"{'-'*70}\n")
            self.result_text.insert(tk.END, f"排除规则: 去掉上述范围内最低15%和最高10%的报价\n")
            self.result_text.insert(tk.END, f"去掉最低: {int(n*0.15)} 家\n")
            self.result_text.insert(tk.END, f"去掉最高: {int(n*0.10)} 家\n")
            self.result_text.insert(tk.END, f"剩余报价: {', '.join([f'{p:.0f}' for p in sorted(filtered)])}\n")
            self.result_text.insert(tk.END, f"剩余数量: {len(filtered)} 家\n\n")
            
            # 3. 综合平均数计算
            self.result_text.insert(tk.END, f"【步骤3】综合平均数计算\n")
            self.result_text.insert(tk.END, f"{'-'*70}\n")
            self.result_text.insert(tk.END, f"3.1 基本统计量:\n")
            self.result_text.insert(tk.END, f"    算术平均数 = {intermediate['arithmetic_mean']:.2f} 元\n")
            self.result_text.insert(tk.END, f"    中位数平均数 = {intermediate['median_mean']:.2f} 元\n")
            self.result_text.insert(tk.END, f"    四分位数平均数 = (Q1 + Q3) / 2\n")
            self.result_text.insert(tk.END, f"                    = ({intermediate['q1']:.2f} + {intermediate['q3']:.2f}) / 2\n")
            self.result_text.insert(tk.END, f"                    = {intermediate['quartile_mean']:.2f} 元\n\n")
            
            if len(valid_prices) < 5:
                self.result_text.insert(tk.END, f"3.2 综合平均数计算:\n")
                self.result_text.insert(tk.END, f"    规则: 有效报价数 < 5 家，综合平均数 = 算术平均数\n")
                self.result_text.insert(tk.END, f"    综合平均数 = {intermediate['comprehensive_mean']:.2f} 元\n\n")
            else:
                self.result_text.insert(tk.END, f"3.2 综合平均数计算:\n")
                self.result_text.insert(tk.END, f"    公式: 综合平均数 = (算术平均数 + 中位数平均数 + 四分位数平均数) / 3\n")
                self.result_text.insert(tk.END, f"    综合平均数 = ({intermediate['arithmetic_mean']:.2f} + {intermediate['median_mean']:.2f} + {intermediate['quartile_mean']:.2f}) / 3\n")
                self.result_text.insert(tk.END, f"    综合平均数 = {intermediate['comprehensive_mean']:.2f} 元\n\n")
            
            # 4. 异常低价警戒线
            self.result_text.insert(tk.END, f"【步骤4】异常低价警戒线计算\n")
            self.result_text.insert(tk.END, f"{'-'*70}\n")
            self.result_text.insert(tk.END, f"下浮值: {float_used:.4f} ({float_used*100:.2f}%)\n")
            self.result_text.insert(tk.END, f"说明: 下浮值在5%-10%区间内选定\n\n")
            self.result_text.insert(tk.END, f"计算公式: 异常低价警戒线 = 综合平均数 × (1 - 下浮值)\n")
            self.result_text.insert(tk.END, f"异常低价警戒线 = {intermediate['comprehensive_mean']:.2f} × (1 - {float_used:.4f})\n")
            self.result_text.insert(tk.END, f"异常低价警戒线 = {alert_line:.2f} 元\n\n")
            
            # 5. 各报价判断
            self.result_text.insert(tk.END, f"{'='*70}\n")
            self.result_text.insert(tk.END, f"各报价判断结果\n")
            self.result_text.insert(tk.END, f"{'='*70}\n")
            self.result_text.insert(tk.END, f"异常低价警戒线: {alert_line:.2f} 元\n")
            self.result_text.insert(tk.END, f"低于此警戒线的报价视为低于投标成本报价\n\n")
            
            self.result_text.insert(tk.END, f"{'报价(元)':<18} {'与警戒线差额':<18} {'判断结果'}\n")
            self.result_text.insert(tk.END, f"{'-'*70}\n")
            
            below_alert = intermediate['below_alert']
            for price in sorted(bid_prices):
                diff = price - alert_line
                if below_alert[price]:
                    status = "⚠️  低于警戒线（需成本分析）"
                    diff_str = f"{diff:.2f}"
                else:
                    status = "✓  正常"
                    diff_str = f"+{diff:.2f}" if diff >= 0 else f"{diff:.2f}"
                self.result_text.insert(tk.END, f"{price:<18.2f} {diff_str:<18} {status}\n")
            
        except ValueError as e:
            messagebox.showerror("输入错误", f"请输入有效的数字：{str(e)}")
        except Exception as e:
            messagebox.showerror("计算错误", f"计算过程中出现错误：{str(e)}")
    
    def clear(self):
        self.bid_entry.delete(0, tk.END)
        self.max_limit_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)
        
        # 重置下浮值参数
        self.float_mode.set("range")
        self.float_min_entry.delete(0, tk.END)
        self.float_min_entry.insert(0, "0.05")
        self.float_max_entry.delete(0, tk.END)
        self.float_max_entry.insert(0, "0.10")
        self.float_fixed_entry.delete(0, tk.END)
        self.float_fixed_entry.insert(0, "0.075")
        self.toggle_float_mode()


def main():
    root = tk.Tk()
    app = AlertLineCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

