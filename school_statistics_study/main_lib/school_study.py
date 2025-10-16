import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.stats import norm
import os
root_path = os.path.dirname(os.path.dirname(__file__))


def read_excel_sheet(file=None):
    '''
    The function will return the lists as DataFrames

    Parameters
    ----------
    file: 'obj' string
        the file name with xls extention [includes the path]

    returns
    -------
    pandas data frames of the excel sheets under test
    '''
    xls_file = pd.ExcelFile(file)
    data_frame = pd.read_excel(xls_file, 'exam_data')
    grade_7 = pd.read_excel(xls_file, 'grade_7')
    # display(data_frame)
    return data_frame, grade_7


def save_csv(headers=None, file_name=None):
    out_file_csv = open(file_name+'.csv', 'w+')
    writer = csv.DictWriter(out_file_csv, fieldnames=headers, delimiter=",")
    writer.writeheader()
    return writer


def get_data_info(list=None,
                  name_to_set=None,
                  name_to_get=None,
                  info_to_set=None):
    condition_name = (list[name_to_set] == info_to_set)
    if condition_name.any():
        out_name = list[condition_name][name_to_get]
    else:
        out_name = None
    return out_name


def generate_data(grades=None,
                  n_size=None,
                  n_sample=None,
                  mean_matrix=None,
                  data_frame=None):
    '''
    The function will generate the required data
    '''
    for g in np.arange(len(grades)):
        file_name = root_path+"/data/statistics_output_"+grades[g]
        csv_writer = save_csv(headers=n_size,
                              file_name=file_name)
        for s in np.arange(n_sample):
            for n in np.arange(len(n_size)):
                data_subset = data_frame[grades[g]].sample(n=n_size[n])
                # get the mean of each class of that sample
                mean_matrix[g][s][n] = np.mean(data_subset)
            g_mean_row = {e: mean_matrix[g][s][i] for i,
                          e in enumerate(n_size)}
            csv_writer.writerow(g_mean_row)
    return mean_matrix


def plot_data(grades=None, n_size=None, g_mean=None):
    for g in np.arange(len(grades)):
        _, axes = plt.subplots(nrows=1, ncols=len(n_size), figsize=(20, 5))
        for n in np.arange(len(n_size)):
            # Histogram the data
            data_hist = g_mean[g][:, n]
            _, bins, _ = axes[n].hist(data_hist,
                                      density=1,
                                      alpha=0.75)
            # best fit of data
            mu, sigma = norm.fit(data_hist)
            data_fit = norm.pdf(bins, mu, sigma)
            axes[n].plot(bins, data_fit, 'r--', linewidth=2)
            # Styles
            txt = (
                grades[g]+": "+r'$\mu = %.2f, \ \sigma = %.2f$' % (mu, sigma)
            )
            axes[n].text(0.95, 0.35, txt, fontsize=12,
                         horizontalalignment='right',
                         verticalalignment='top', transform=axes[n].transAxes,
                         bbox=dict(boxstyle='round',
                                   facecolor='wheat',
                                   alpha=0.2))
            axes[n].set_ylabel("Frequency")
            axes[n].set_xlabel("Estimate of Mean")
            axes[n].autoscale(enable=True, axis='x', tight=None)
            text_title = "Sampling distribution for (N={})".format(n_size[n])
            axes[n].set_title(text_title,
                              fontsize=12)
            # axes[n].set_xlim([12, 16])
            axes[n].grid(True)
            plt.tight_layout()
            fig_name = root_path+"/output/statistics_output_"+grades[g]+".png"
            plt.savefig(fig_name)


def main():
    '''
     A school has 1200 students, with 200 students each in grades 7 through 12.
     The population distribution is  definitely not normal.
     lets prepare different samples [20, 60, 80,100, 150, 200]
    '''
    grades = ["Grade_7", "Grade_8", "Grade_9",
              "Grade_10", "Grade_11", "Grade_12"]
    n_size = [20, 60, 80, 100, 150, 200]
    n_sample = 1000
    n_students = 36
    output_file = root_path+"/data/data-entry.xlsx"
    g_mean = np.zeros((len(grades), n_sample, len(n_size)))
    data_frame, grade_7 = read_excel_sheet(file=output_file)
    g_mean = generate_data(grades=grades, n_size=n_size,
                           n_sample=n_sample,
                           mean_matrix=g_mean, data_frame=data_frame)
    plot_data(grades=[grades[0]], n_size=n_size, g_mean=g_mean)

    novel_students = get_data_info(list=grade_7,
                                   name_to_set="novel_student",
                                   name_to_get="exam_results",
                                   info_to_set=1)
    novel_students_sample = novel_students.sample(n=n_students)
    grade_7_sample = grade_7["exam_results"].sample(n=n_students)
    print(f"Sample mean for {n_students} students in novel students=",
          np.mean(novel_students_sample))
    print(f"Sample mean for {n_students} students in whole sample=",
          np.mean(grade_7_sample))


if __name__ == "__main__":
    main()
