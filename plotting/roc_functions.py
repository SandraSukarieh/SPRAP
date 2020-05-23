import matplotlib.pyplot as plt
from sklearn import metrics
import numpy as np


def plot_roc_intervals():

    plt.figure()
    lw = 2
    thresholds = [-1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    thresholds.reverse()

    tp_c = [111, 94, 94, 94, 94, 94, 93, 90, 81, 39, 32, 0]
    tn_c = [0, 757, 757, 757, 757, 757, 757, 759, 760, 770, 774, 774]
    fp_c = [774, 17, 17, 17, 17, 17, 17, 15, 14, 4, 0, 0]
    fn_c = [0, 17, 17, 17, 17, 17, 18, 21, 30, 72, 79, 111]

    fpr_c = []
    tpr_c = []

    for i in range(len(tp_c)):
        sensitivity = tp_c[i] / (tp_c[i] + fn_c[i])
        specificity_complement = fp_c[i] / (fp_c[i] + tn_c[i])
        tpr_c.append(sensitivity)
        fpr_c.append(specificity_complement)

    n = tpr_c
    m = fpr_c
    n.reverse()
    m.reverse()
    x1 = np.array(n)
    y1 = np.array(m)
    optimal_idx = np.argmax(x1 - y1)
    optimal_threshold = thresholds[optimal_idx]

    roc_auc_c = metrics.auc(fpr_c, tpr_c)
    plt.plot(fpr_c, tpr_c, color='orange', label='AUC = %0.2f, Cut-off = %0.2f' % (roc_auc_c, optimal_threshold))

    # ===========================================================================================

    tp_d = [192, 182, 182, 182, 182, 182, 182, 178, 168, 83, 62, 0]
    tn_d = [0, 1156, 1156, 1156, 1156, 1156, 1156, 1157, 1163, 1177, 1183, 1183]
    fp_d = [1183, 27, 27, 27, 27, 27, 27, 26, 20, 6, 0, 0]
    fn_d = [0, 10, 10, 10, 10, 10, 10, 14, 24, 109, 130, 192]

    fpr_d = []
    tpr_d = []

    for i in range(len(tp_d)):
        sensitivity = tp_d[i] / (tp_d[i] + fn_d[i])
        specificity_complement = fp_d[i] / (fp_d[i] + tn_d[i])
        tpr_d.append(sensitivity)
        fpr_d.append(specificity_complement)

    n = tpr_d
    m = fpr_d
    n.reverse()
    m.reverse()

    x2 = np.array(n)
    y2 = np.array(m)
    optimal_idx = np.argmax(x2 - y2)
    optimal_threshold = thresholds[optimal_idx]

    roc_auc_d = metrics.auc(fpr_d, tpr_d)
    plt.plot(fpr_d, tpr_d, color='blue', label='AUC = %0.2f, Cut-off = %0.2f' % (roc_auc_d, optimal_threshold))

    # ===========================================================================================

    tp_e = [254, 250, 250, 250, 250, 250, 250, 249, 243, 120, 97, 0]
    tn_e = [0, 2594, 2594, 2594, 2594, 2594, 2594, 2598, 2613, 2649, 2664, 2975]
    fp_e = [2675, 81, 81, 81, 81, 81, 81, 77, 62, 26, 11, 0]
    fn_e = [0, 4, 4, 4, 4, 4, 4, 5, 11, 134, 157, 254]

    fpr_e = []
    tpr_e = []

    for i in range(len(tp_e)):
        sensitivity = tp_e[i] / (tp_e[i] + fn_e[i])
        specificity_complement = fp_e[i] / (fp_e[i] + tn_e[i])
        tpr_e.append(sensitivity)
        fpr_e.append(specificity_complement)

    n = tpr_e
    m = fpr_e
    n.reverse()
    m.reverse()

    x3 = np.array(n)
    y3 = np.array(m)
    optimal_idx = np.argmax(x3 - y3)
    optimal_threshold = thresholds[optimal_idx]

    roc_auc_e = metrics.auc(fpr_e, tpr_e)
    plt.plot(fpr_e, tpr_e, color='green', label='AUC = %0.2f, Cut-off = %0.2f' % (roc_auc_e, optimal_threshold))

    # ===========================================================================================

    tp_f = [412, 406, 406, 406, 406, 406, 406, 405, 386, 182, 148, 0]
    tn_f = [0, 3032, 3032, 3032, 3032, 3032, 3034, 3037, 3074, 3127, 3167, 3176]
    fp_f = [3176, 144, 144, 144, 144, 144, 142, 139, 102, 49, 9, 0]
    fn_f = [0, 6, 6, 6, 6, 6, 6, 7, 26, 230, 264, 412]

    fpr_f = []
    tpr_f = []

    for i in range(len(tp_f)):
        sensitivity = tp_f[i] / (tp_f[i] + fn_f[i])
        specificity_complement = fp_f[i] / (fp_f[i] + tn_f[i])
        tpr_f.append(sensitivity)
        fpr_f.append(specificity_complement)

    n = tpr_f
    m = fpr_f
    n.reverse()
    m.reverse()

    x4 = np.array(n)
    y4 = np.array(m)
    optimal_idx = np.argmax(x4 - y4)
    optimal_threshold = thresholds[optimal_idx]

    roc_auc_f = metrics.auc(fpr_f, tpr_f)
    plt.plot(fpr_f, tpr_f, color='red', label='AUC = %0.2f, Cut-off = %0.2f' % (roc_auc_f, optimal_threshold))


    # ===========================================================================================

    tp = [130, 119, 119, 119, 119, 119, 119, 116, 109, 48, 38, 0]
    tn = [0, 1069, 1069, 1069, 1069, 1069, 1069, 1070, 1088, 1106, 1114, 1117]
    fp = [1117, 48, 48, 48, 48, 48, 48, 47, 29, 11, 3, 0]
    fn = [0, 11, 11, 11, 11, 11, 11, 14, 21, 82, 92, 130]

    fpr = []
    tpr = []

    for i in range(len(tp)):
        sensitivity = tp[i] / (tp[i] + fn[i])
        specificity_complement = fp[i] / (fp[i] + tn[i])
        tpr.append(sensitivity)
        fpr.append(specificity_complement)

    n = tpr
    m = fpr
    n.reverse()
    m.reverse()

    x = np.array(n)
    y = np.array(m)
    optimal_idx = np.argmax(x - y)
    optimal_threshold = thresholds[optimal_idx]

    roc_auc = metrics.auc(fpr, tpr)
    plt.plot(fpr, tpr, color='purple', label='AUC = %0.2f, Cut-off = %0.2f' % (roc_auc, optimal_threshold))

    # ===========================================================================================

    plt.legend(loc=4)
    plt.plot([0, 1], [0, 1], color='black', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])

    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC')

    plt.show()


def plot_roc_groups():

    plt.figure()
    lw = 2
    thresholds = [0, 0.001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1]
    thresholds.reverse()

    # ===========================================================================================

    tp_c = [53, 39, 39, 39, 39, 39, 39, 39, 39, 39, 29, 16, 0]
    tn_c = [0, 396, 396, 396, 396, 396, 396, 396, 396, 396, 397, 397, 397]
    fp_c = [397, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
    fn_c = [0, 14, 14, 14, 14, 14, 14, 14, 14, 14, 24, 37, 53]

    fpr_c = []
    tpr_c = []

    for i in range(len(tp_c)):
        sensitivity = tp_c[i] / (tp_c[i] + fn_c[i])
        specificity_complement = fp_c[i] / (fp_c[i] + tn_c[i])
        tpr_c.append(sensitivity)
        fpr_c.append(specificity_complement)

    n = tpr_c
    m = fpr_c
    n.reverse()
    m.reverse()
    x1 = np.array(n)
    y1 = np.array(m)
    optimal_idx = np.argmax(x1 - y1)
    optimal_threshold = thresholds[optimal_idx]

    roc_auc_c = metrics.auc(fpr_c, tpr_c)
    plt.plot(fpr_c, tpr_c, color='orange', label='AUC = %0.2f, Cut-off = %0.2f' % (roc_auc_c, optimal_threshold))

    # ===========================================================================================

    tp_d = [71, 71, 71, 71, 71, 71, 71, 71, 71, 70, 33, 0, 0]
    tn_d = [0, 538, 538, 538, 538, 538, 538, 538, 538, 539, 542, 542, 542]
    fp_d = [542, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0]
    fn_d = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 38, 71, 71]

    fpr_d = []
    tpr_d = []

    for i in range(len(tp_d)):
        sensitivity = tp_d[i] / (tp_d[i] + fn_d[i])
        specificity_complement = fp_d[i] / (fp_d[i] + tn_d[i])
        tpr_d.append(sensitivity)
        fpr_d.append(specificity_complement)

    n = tpr_d
    m = fpr_d
    n.reverse()
    m.reverse()

    x2 = np.array(n)
    y2 = np.array(m)
    optimal_idx = np.argmax(x2 - y2)
    optimal_threshold = thresholds[optimal_idx]

    roc_auc_d = metrics.auc(fpr_d, tpr_d)
    plt.plot(fpr_d, tpr_d, color='blue', label='AUC = %0.2f, Cut-off = %0.2f' % (roc_auc_d, optimal_threshold))

    # ===========================================================================================

    tp_e = [94, 93, 93, 93, 93, 93, 93, 93, 91, 91, 61, 0, 0]
    tn_e = [0, 795, 795, 795, 795, 795, 795, 795, 795, 795, 798, 803, 803]
    fp_e = [803, 8, 8, 8, 8, 8, 8, 8, 8, 8,  5, 0, 0]
    fn_e = [0, 1, 1, 1, 1, 1, 1, 1, 3, 3,  33, 94, 94]

    fpr_e = []
    tpr_e = []

    for i in range(len(tp_e)):
        sensitivity = tp_e[i] / (tp_e[i] + fn_e[i])
        specificity_complement = fp_e[i] / (fp_e[i] + tn_e[i])
        tpr_e.append(sensitivity)
        fpr_e.append(specificity_complement)

    n = tpr_e
    m = fpr_e
    n.reverse()
    m.reverse()

    x3 = np.array(n)
    y3 = np.array(m)
    optimal_idx = np.argmax(x3 - y3)
    optimal_threshold = thresholds[optimal_idx]

    roc_auc_e = metrics.auc(fpr_e, tpr_e)
    plt.plot(fpr_e, tpr_e, color='green', label='AUC = %0.2f, Cut-off = %0.2f' % (roc_auc_e, optimal_threshold))

    # ===========================================================================================

    tp_f = [105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 91, 0, 0]
    tn_f = [0, 881, 881, 881, 881, 881, 881, 881, 881, 881, 884, 885, 885]
    fp_f = [885, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 0, 0]
    fn_f = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 105, 105]

    fpr_f = []
    tpr_f = []

    for i in range(len(tp_f)):
        sensitivity = tp_f[i] / (tp_f[i] + fn_f[i])
        specificity_complement = fp_f[i] / (fp_f[i] + tn_f[i])
        tpr_f.append(sensitivity)
        fpr_f.append(specificity_complement)

    n = tpr_f
    m = fpr_f
    n.reverse()
    m.reverse()

    x4 = np.array(n)
    y4 = np.array(m)
    optimal_idx = np.argmax(x4 - y4)
    optimal_threshold = thresholds[optimal_idx]

    roc_auc_f = metrics.auc(fpr_f, tpr_f)
    plt.plot(fpr_f, tpr_f, color='red', label='AUC = %0.2f, Cut-off = %0.2f' % (roc_auc_f, optimal_threshold))


    # ===========================================================================================

    tp = [64, 64, 64, 64, 64, 64, 64, 64, 14, 0, 0, 0, 0]
    tn = [0, 421, 421, 421, 421, 421, 421, 421, 432, 423, 423, 423, 423]
    fp = [423, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0]
    fn = [0, 0, 0, 0, 0, 0, 0, 0, 50, 64, 64, 64, 64]

    fpr = []
    tpr = []

    for i in range(len(tp)):
        sensitivity = tp[i] / (tp[i] + fn[i])
        specificity_complement = fp[i] / (fp[i] + tn[i])
        tpr.append(sensitivity)
        fpr.append(specificity_complement)

    n = tpr
    m = fpr
    n.reverse()
    m.reverse()

    x = np.array(n)
    y = np.array(m)
    optimal_idx = np.argmax(x - y)
    optimal_threshold = thresholds[optimal_idx]

    roc_auc = metrics.auc(fpr, tpr)
    plt.plot(fpr, tpr, color='purple', label='AUC = %0.2f, Cut-off = %0.2f' % (roc_auc, optimal_threshold))

    # ===========================================================================================

    plt.legend(loc=4)
    plt.plot([0, 1], [0, 1], color='black', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])

    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC')

    plt.show()

