import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import Tuple, List


def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    读取并处理电影数据
    
    Args:
        file_path: CSV文件路径
        
    Returns:
        处理后的DataFrame
    """
    df = pd.read_csv(
        file_path,
        usecols=["电影名", "年份", "上映时间", "语言", "类型", "评分"],
        dtype={'年份': 'Int64'}
    )
    
    # 处理缺失值：用上映时间的前4位填充年份
    df['年份'] = df['年份'].fillna(df['上映时间'].str[:4])
    
    return df


def get_yearly_movie_count(df: pd.DataFrame) -> Tuple[List[int], List[int]]:
    """
    统计每年上映的电影数量
    
    Args:
        df: 电影数据DataFrame
        
    Returns:
        x轴（年份列表）和y轴（数量列表）
    """
    year_count = df.groupby('年份')['年份'].count()
    
    min_year = year_count.index.min()
    max_year = year_count.index.max()
    
    x = [i for i in range(min_year, max_year + 1)]
    y = [year_count.get(i, 0) for i in x]
    
    return x, y


def get_language_distribution(df: pd.DataFrame) -> Tuple[List[str], List[int]]:
    """
    统计不同语言的电影数量分布
    
    Args:
        df: 电影数据DataFrame
        
    Returns:
        x轴（语言列表）和y轴（数量列表）
    """
    language_count = df.groupby('语言')['语言'].count().sort_values(ascending=False)
    
    x = language_count.index.tolist()
    y = language_count.values.tolist()
    
    return x, y


def get_type_distribution(df: pd.DataFrame) -> Tuple[List[str], List[int]]:
    """
    统计不同类型电影的分布（支持多类型）
    
    Args:
        df: 电影数据DataFrame
        
    Returns:
        x轴（类型列表）和y轴（数量列表）
    """
    type_count = {}
    for types in df['类型'].str.split(','):
        for movie_type in types:
            if movie_type in type_count:
                type_count[movie_type] += 1
            else:
                type_count[movie_type] = 1
    
    x = list(type_count.keys())
    y = list(type_count.values())
    
    return x, y


def get_score_distribution(df: pd.DataFrame) -> Tuple[List, List]:
    """
    统计评分分布，合并占比小于2%的小数据为"其他"
    
    Args:
        df: 电影数据DataFrame
        
    Returns:
        x轴（评分标签列表）和y轴（数量列表）
    """
    score_count = df.groupby('评分')['评分'].count()
    
    total = score_count.sum()
    large_score = score_count.loc[score_count >= total * 0.02]
    small_score = score_count.loc[score_count < total * 0.02]
    
    if small_score.shape[0] > 0:
        large_score = large_score.copy()
        large_score['其他'] = small_score.sum()
    
    x = large_score.index.tolist()
    y = large_score.values.tolist()
    
    return x, y


def plot_yearly_trend(ax: Axes, x: List[int], y: List[int]) -> None:
    """
    绘制每年上映电影数量折线图
    
    Args:
        ax: matplotlib坐标轴对象
        x: 年份列表
        y: 数量列表
    """
    ax.plot(x, y)
    ax.set_title('每年上映电影数量')
    ax.set_xlabel('年份')
    ax.set_ylabel('数量')
    ax.set_xticks(x[::10])
    ax.set_yticks([i for i in range(0, 31, 3)])
    ax.grid(True, linestyle='--', alpha=0.5)


def plot_language_distribution(ax: Axes, x: List[str], y: List[int]) -> None:
    """
    绘制不同语言电影数量柱状图
    
    Args:
        ax: matplotlib坐标轴对象
        x: 语言列表
        y: 数量列表
    """
    ax.bar(x, y)
    ax.set_title('不同语言的电影数量')
    ax.set_xlabel('语言')
    ax.set_ylabel('数量')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle='--', alpha=0.5)


def plot_type_distribution(ax: Axes, x: List[str], y: List[int]) -> None:
    """
    绘制不同类型电影数量柱状图
    
    Args:
        ax: matplotlib坐标轴对象
        x: 类型列表
        y: 数量列表
    """
    ax.bar(x, y)
    ax.set_title('不同类型的电影数量')
    ax.set_xlabel('类型')
    ax.set_ylabel('数量')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle='--', alpha=0.5)


def plot_score_distribution(ax: Axes, x: List, y: List) -> None:
    """
    绘制评分分布饼状图
    
    Args:
        ax: matplotlib坐标轴对象
        x: 评分标签列表
        y: 数量列表
    """
    ax.pie(y, labels=x, autopct='%1.1f%%')
    ax.set_title('不同评分的电影占比')
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    ax.axis('equal')


def create_visualization(
    year_data: Tuple[List[int], List[int]],
    language_data: Tuple[List[str], List[int]],
    type_data: Tuple[List[str], List[int]],
    score_data: Tuple[List, List],
    save_path: str = "Data/movie.png"
) -> None:
    """
    创建并保存四合一可视化图表
    
    Args:
        year_data: 年份统计数据 (x, y)
        language_data: 语言统计数据 (x, y)
        type_data: 类型统计数据 (x, y)
        score_data: 评分统计数据 (x, y)
        save_path: 图片保存路径
    """
    # 设置中文显示
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建画布
    figure, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 20), dpi=100)
    figure.suptitle("电影信息", fontsize=23, x=0.5, y=0.95)
    
    axes1: Axes = axes[0, 0]
    axes2: Axes = axes[0, 1]
    axes3: Axes = axes[1, 0]
    axes4: Axes = axes[1, 1]
    
    # 绘制四个子图
    plot_yearly_trend(axes1, *year_data)
    plot_language_distribution(axes2, *language_data)
    plot_type_distribution(axes3, *type_data)
    plot_score_distribution(axes4, *score_data)
    
    # 保存图片
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()


def main():
    """主函数：执行完整的数据分析和可视化流程"""
    # 1. 加载和处理数据
    print("正在加载数据...")
    df = load_and_process_data("Data/movies.csv")
    print(f"数据加载完成，共 {len(df)} 条记录\n")
    
    # 2. 统计分析
    print("正在进行数据分析...")
    year_data = get_yearly_movie_count(df)
    language_data = get_language_distribution(df)
    type_data = get_type_distribution(df)
    score_data = get_score_distribution(df)
    print("数据分析完成\n")
    
    # 3. 可视化
    print("正在生成可视化图表...")
    create_visualization(
        year_data=year_data,
        language_data=language_data,
        type_data=type_data,
        score_data=score_data,
        save_path="Data/movie.png"
    )
    print("图表已保存到 Data/movie.png")


if __name__ == "__main__":
    main()
