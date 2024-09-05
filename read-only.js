// 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


{#====My Cats Start====#}
{#{% if cats %}#}
{#    <section class="cat-container container">#}
{#        <div class="cat-container-header bg-success pt-4 pb-4 pr-1 pl-1">#}
{#            <h4 class="m-2">#}
{#                CATs Participated#}
{#            </h4>#}
{#        </div>#}
{#        <div class="cat-container-card-holder flex pt-4 pb-4">#}
{#            {% for cat in cats %}#}
{#                <div class="card">#}
{#                    <div class="card-footer">#}
{#                        <h5 class="font-weight-bolder">#}
{#                            <span class="p-2 btn btn-secondary">CAT Id: {{ cat.cat.cat_id }}</span>#}
{#                        </h5>#}
{#                    #}
{#                        <p>CAT Name: {{ cat.cat.name }}</p>#}
{#                        <p>Start Date: {{ cat.cat.start }}</p>#}
{#                        <p>End Date: {{ cat.cat.end }}</p>#}
{#                        {% if cat.cat.end > end_time_check %}                            #}
{#                            <a class="btn btn-success w-100" href="{% url 'student-cat-view-url' cat.cat.id %}">Open</a>#}
{#                        {% else %}#}
{#                            <p>#}
{#                                Score: {{ answers.count }} out of #}
{#                            {% for question in questions %}#}
{#                                {% if question.cat == cat.cat %}#}
{#                                	{{ question.count }}#}
{#                                {% endif %} #}
{#                            	#}
{#                            {% endfor %}                            #}
{#                            </p>#}
{#                            <a class="btn btn-secondary w-100" href="">View Results</a>#}
{#                        {% endif %}#}
{#                    </div>#}
{#                </div>#}
{#            {% endfor %}#}
{#        </div>#}
{#    </section>#}
{#{% else %}#}
{#    <h3 class="text-center w-100">You have not participated in any CAT.</h3>#}
{#{% endif %}#}
{#====My Cats End====#}