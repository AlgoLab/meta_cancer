def fast_anc_desc_f1(true_trees, tool_trees, mut):
    ad_f1_scores = []
    ids = []
    mut = None

    for i in range(len(true_trees)):

        ids.append(i)
        tree = true_trees[i]
        tool = tool_trees[i]

        mut = len(tree.mut_to_node)

        ad_tp = 0
        ad_fp = 0
        ad_fn = 0

        mutations = list(range(1, mut + 1))
        ad_true_tp_pairs = dict()
        ad_true_tn_pairs = dict()
        for a in mutations:
            for b in mutations:
                # print('ground',a,b)
                if tree.is_ancestor(str(a), str(b)):
                    ad_true_tp_pairs[(a,b)] = True
                else:
                    ad_true_tn_pairs[(a,b)] = True

        ad_tool_tp_pairs = dict()
        ad_tool_tn_pairs = dict()
        for a in mutations:
            for b in mutations:
                # print('tool',a,b)
                try:
                    if tool.is_ancestor(str(a), str(b)):
                        ad_tool_tp_pairs[(a,b)] = True
                    else:
                        ad_tool_tn_pairs[(a,b)] = True
                except:
                    pass
        
        
        for pair in ad_tool_tp_pairs:
            # print('pair-tp', pair)
            if pair in ad_true_tp_pairs:
                ad_tp += 1
            elif pair in ad_true_tn_pairs:
                ad_fp += 1
        for pair in ad_tool_tn_pairs:
            if pair in ad_true_tp_pairs:
                ad_fn += 1

        # print('tp %d, fp %d, fn %d' % (ad_tp, ad_fp, ad_fn))

        try:
            ad_pre = float(ad_tp) / (ad_tp + ad_fp)
            ad_rec = float(ad_tp) / (ad_tp + ad_fn)
            # print('pre-rec computed')
        
            score = 2*((ad_pre*ad_rec)/(ad_pre+ad_rec))
            ad_f1_scores.append(score)
            print('sim %d, anc desc: %f' % (i, score))
        except ZeroDivisionError:
            print('Warning: division by zero while computing F1-score of Ancestor-Descendant. This result will be set to 0')
            ad_f1_scores.append(0)
        
    return ad_f1_scores

def fast_diff_lin_f1(true_trees, tool_trees, mut):
    f1_scores = []
    ids = []

    mut = None
    
    for i in range(len(true_trees)):
        ids.append(i)
        tree = true_trees[i]
        tool = tool_trees[i]

        mut = len(tree.mut_to_node)

        tp = 0
        tn = 0
        fp = 0
        fn = 0

        mutations = list(range(1, mut + 1))
        true_tp_pairs = dict()
        true_tn_pairs = dict()
        for a in mutations:
            for b in mutations:
                # print('ground', a,b)
                if not tree.is_ancestor(str(a), str(b)):
                    true_tp_pairs[(a,b)] = True
                else:
                    true_tn_pairs[(a,b)] = True
        # print('true: tp %d\ttn %d' % (len(true_tp_pairs), len(true_tn_pairs)))

        tool_tp_pairs = dict()
        tool_tn_pairs = dict()
        for a in mutations:
            for b in mutations:
                # print('tool', a,b)
                try:
                    if not tool.is_ancestor(str(a), str(b)):
                        tool_tp_pairs[(a,b)] = True
                    else:
                        tool_tn_pairs[(a,b)] = True
                except:
                    pass
        # print('true: tp %d\ttn %d' % (len(tool_tp_pairs), len(tool_tn_pairs)))
        
        for pair in tool_tp_pairs:
            # print('pair-tp', pair)
            if pair in true_tp_pairs:
                tp += 1
            elif pair in true_tn_pairs:
                fp += 1
        for pair in tool_tn_pairs:
            # print('pair-tn', pair)
            # if pair in true_tn_pairs:
            #     tn += 1
            if pair in true_tp_pairs:
                fn += 1

        # print('tp %d, fp %d, fn %d' % (tp, fp, fn))
        try:
            pre = float(tp) / (tp + fp)
            rec = float(tp) / (tp + fn)

            score = 2*((pre*rec)/(pre+rec))
            f1_scores.append(score)
            print('sim %d, diff lin: %f' % (i, score))
        except ZeroDivisionError:
            print('Warning: division by zero while computing F1-score of Different-Lineages. This result will be set to 0')
            f1_scores.append(0)

        # score = 
        # print('sim %d, diff lin: %f' % (i,score))
        # f1_scores.append(score)
        
    return f1_scores


def parsimony_score(true, tool):
    f01 = 0
    f10 = 0
    for i in range(true.shape[0]):
        for j in range(true.shape[1]):
            if true[i][j] == 1 and tool[i][j] == 0:
                f10 += 1
            if true[i][j] == 0 and tool[i][j] == 1:
                f01 += 1
    
    return (f01+f10, f01, f10)